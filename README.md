# dask-distributed-templates

dask.distributedの使い方と、具体例集です

## setup

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
Schedulerは分析を実行するマシンとかでいいはず
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
上記の簡単な足し算を並列マシン（worker数の増加）でやろうとすると、処理時間がほぼ反比例の関係で下がるので、正しく分散処理できていることが確認できる。

<p align="center">
  <img width="500px" src="https://user-images.githubusercontent.com/4949982/37890533-d730c30e-310b-11e8-964a-d082654f64ef.png">
</p>
