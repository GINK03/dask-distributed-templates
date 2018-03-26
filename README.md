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
