# dask-distributed-templates

dask.distributedの使い方と、具体例集です

## Dask.Distributedの簡単な理解
一種の分散処理フレームワークになっており、便利です。  
Celeryとかでもやったことをがあるのですが、Remote Procedureのそれよりまともでより整理された方法で、concurrent.futureのリモート版とも考えられます。  

<p align="center">
  <img width="550px" src="https://user-images.githubusercontent.com/4949982/37904798-c2d3f6d4-3137-11e8-9ffd-fb9af56822d8.png">
</p>

## ネットワークのsetup

**daskのインストール**  
```console
$ sudo pip3 install dask distribute --upgrade
```

**nodeのインストール(Ubuntu)**  
注：パッケージが微妙に古くてpip経由の方がいい
```console
$ sudo apt install python3-distributed
```

## Dask SchedulerとWorkerのセットアップ
Schedulerは分析を実行するマシンとかでもいいです
```console
$ dask-scheduler
Start scheduler at 192.168.14.15:8786
```

**portのチェック**  
```console
$ nc -v -w 1 192.168.14.15 -z 8786
```

Workerは命令を受けるマシンなので、別のマシンなどがよい
```console
$ dask-worker ${SCHEDULER}:8786
```

**クライアントのCPU数**  

マルチコアの場合、CPU数を多めに取ってやったりする

nprocsオプションで最大のworkerでの並列数を指定できます  
```console
$ dask-worker ${SCHEDULER}:8786 --nprocs 12
```

## 簡単な命令(数字を増やすだけ)
```python
from distributed import Client

client = Client('192.168.14.13:8786')

def inc(x):
  for i in range(10000000):
    x += i
  return x

x = client.submit(inc, 10)
print(x.result())

L = client.map(inc, range(1000))

ga = client.gather(L)
print(ga)
```

## Dask.Distributedの並列マシン数と、速度の関係
上記の簡単な足し算を並列マシン（worker数の増加）でやろうとすると、処理時間がほぼ反比例の関係で下がるので、効率的に分散処理できていることが確認できます。

<p align="center">
  <img width="500px" src="https://user-images.githubusercontent.com/4949982/37890533-d730c30e-310b-11e8-964a-d082654f64ef.png">
</p>

## 分散した命令の結果を受け取る２つの方法
clientにmapされた命令はschedulerが管理して分散処理されますが、内部で、マシン台数かにchunkされているらしく、順番が一気に結果を見る(gather)のも、個別にみる(result)のもあまり変わりがないようです。

gatherという関数で一気に集められますが戻り値が多いときには、オンメモリにするのが難しいので、挙動が不安です。  
```python
L = client.map(inc, range(1000))
ga = client.gather(L)
```

resultで一個一個取っていく方法は、ブロッキングされているので、遅いですがメモリ節約にはなりそうです
```python
L = client.map(inc, args)
for l in L:
  print(l.result())
```

## 機械学習のモデルのグリッドサーチでも便利
機械学習のパラメータを少しずつ変えながらもっとも、パフォーマンスが良いパラメータを総当りで探すグリッドサーチというものあって、マシンパワーでゴリ押ししてしまうのが都合がいいのです。  

複数台のworkerでグリッドサーチさせると、そのマシンの台数分だけ減らせます。  

代表的なUCIのadult incomeデータセットでランダムフォレストでパラメータを2x10x10x15=3000通りという膨大なパラメータサーチであっても、割と早く終わらせることができます。  

以下のコードの例では、パラメータの組み合わせを作って、分散処理で評価させています。  

関数doはworkerで実行されて、ホームディレクトリ以下のデータセットを読み込んで、引数に与えられたRandomForestのパラメータを適応して学習し、テストデータでの精度を見ています。  

```python
def do(param):
  dataset = pickle.load(open(f'{os.environ["HOME"]}/dataset.pkl', 'rb'))
  Xs, ys, Xst, yst = dataset

  criterion, n_estimators, max_features, max_depth = param
  model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_features=max_features, max_depth=max_depth)
  model.fit(Xs, ys)
  ysp = model.predict(Xst)
  acc = accuracy_score(yst, ysp)
  print(acc)
  return [acc, list(param)]

params = []
for cri in ['gini', 'entropy']:
  for n_esti in range(5,15):
    for max_features in range(10,20):
      for max_depth in range(4, 20):
        params.append( (cri, n_esti, max_features, max_depth) )
L = client.map(do, params)

ga = client.gather(L)
```

**adult incomeのデータを学習可能かデータに変換**  
```console
$ python3 parse-adult.py
```
**出力されたdataset.pklを各workerのホームディレクトに配置**  

**workerの台数で分散処理してグリッドサーチ**  
```console
$ time python3 adult.py
...
real    2m24.923s
user    0m5.950s
sys     0m0.951s
```
10分以上かかる処理が2分程度に圧縮できました！

## dask.distributedで注意すべき点
dask.distributedで関数の引数に大きすぎるデータ（100MByte）を超えるものを投入すると警告が出るし、転送も早くありません。  

そのため、なんらかローカルで対象となるデータを共有している必要があり、HDFSやS3, cloudstrageなどとは相性がよい設計です。（DaskがリソースマネージされたPandasなのでそうなのですが）  

S3とかに格納されたデータを一気に処理するときなど、便利そうです

## 金銭的な比較
今現在、私の個人サーバは6core 12threadのRyzen 1600Xが5台あって、30core 60threadで動作します。  

2018/03現在、これはおおよそ2万円なので、１０万円程度でこの仕組が購入できたことになります。  

同等のスペックである[Epyc 7551p](https://www.amd.com/en/products/cpu/amd-epyc-7551p)は$2100なので、おおよそ20万円で、半額程度で手に入れることができました。  

もちろん、分散させないで一大のマシンで処理するメリットとかあると思うのですが、こんな大規模計算は稀だし、必要なときにdask-workerを立ち上げてクラスタに組み込めるのはメリットです。  

## Dask(+Dask.Distributed)の使い所
Apche Sparkと競合するような位置づけですが、Daks.Distributedのその簡単にデプロイできることと、Apache Sparkを用意するまででもないときとかよいんではないか、みたいに言われているようです。  

私は、HadoopやDataFlow(Apache Beam)が結構好きで得意なので、Sparkをあんまり使わないですが、ここまで大げさに分散処理する必要が無いときにDask(+Dask.Distributed)は良さそうですね。

