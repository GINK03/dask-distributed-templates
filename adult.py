from distributed import Client
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import sys, os
client = Client('192.168.14.13:8786')


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

import json
json.dump( ga, open('ga.json', 'w'), indent=2)
print(ga)
