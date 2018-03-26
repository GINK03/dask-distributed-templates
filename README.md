# dask-distributed-templates

dask.distributedの使い方と、具体例集です

## setup

**daskのインストール**  
```console
$ sudo pip3 install dask
```

**nodeのインストール(Ubuntu)**  
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
$ dask-worker ${SCHEDULER-HOST}:8786
```
