import re

fp = open('adult.data')

# 最初にカテゴリ変数の数をカウントする
cats = set()

for c in ['age', 'fnlwgt', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']:
  cats.add(c)

for line in fp:
  es = re.split(r', ', line.strip())
  if len(es) <= 10:
    continue
  print(es)
  age = es.pop(0) # continuous
  workclass = es.pop(0)
  fnlwgt = es.pop(0) # continuous
  education = es.pop(0) 
  education_num = es.pop(0) # continuous
  marital_status = es.pop(0)
  occupation = es.pop(0)
  relationship = es.pop(0)
  race = es.pop(0)
  sex = es.pop(0)
  capital_gain = es.pop(0) # continuous
  capital_loss = es.pop(0) # continuous
  hours_per_week = es.pop(0) # continuous
  native_country = es.pop(0)
  income = es.pop(0)
  
  cats.add(workclass)
  cats.add(education)
  cats.add(marital_status)
  cats.add(occupation)
  cats.add(relationship)
  cats.add(race)
  cats.add(sex)
  cats.add(native_country)

cat_index = {}
for cat in cats:
  cat_index[cat] = len(cat_index)

print(cat_index)

Xs, ys = [], []
fp = open('adult.data')
for line in fp:
  x = [0.]*len(cat_index)
  es = re.split(r', ', line.strip())
  if len(es) <= 10:
    continue
  age = float(es.pop(0)) # continuous
  x[ cat_index['age'] ] = age
  workclass = es.pop(0)
  x[ cat_index[workclass] ] = 1.0
  fnlwgt = float(es.pop(0)) # continuous
  x[ cat_index['fnlwgt'] ] = fnlwgt
  education = es.pop(0) 
  x[ cat_index[education] ] = 1.0
  education_num = float(es.pop(0)) # continuous
  x[ cat_index['education_num'] ] = education_num
  marital_status = es.pop(0)
  x[ cat_index[marital_status] ] = 1.0
  occupation = es.pop(0)
  x[ cat_index[occupation] ] = 1.0
  relationship = es.pop(0)
  x[ cat_index[relationship] ] = 1.0
  race = es.pop(0)
  x[ cat_index[race] ] = 1.0
  sex = es.pop(0)
  x[ cat_index[sex] ] = 1.0
  capital_gain = float(es.pop(0)) # continuous
  x[ cat_index['capital_gain'] ] = capital_gain
  capital_loss = float(es.pop(0)) # continuous
  x[ cat_index['capital_loss'] ] = capital_loss
  hours_per_week = float(es.pop(0)) # continuous
  x[ cat_index['hours_per_week'] ] = hours_per_week
  native_country = es.pop(0)
  x[ cat_index[native_country] ] = 1.0
  income = es.pop(0)
  print( x )
  y = 1.0 if '>50K' in income else 0.0
  print(y)
  ys.append( y )
  Xs.append( x )

Xst, yst = [], []
fp = open('adult.test')
for line in fp:
  x = [0.]*len(cat_index)
  es = re.split(r', ', line.strip())
  if len(es) <= 10:
    continue
  age = float(es.pop(0)) # continuous
  x[ cat_index['age'] ] = age
  workclass = es.pop(0)
  x[ cat_index[workclass] ] = 1.0
  fnlwgt = float(es.pop(0)) # continuous
  x[ cat_index['fnlwgt'] ] = fnlwgt
  education = es.pop(0) 
  x[ cat_index[education] ] = 1.0
  education_num = float(es.pop(0)) # continuous
  x[ cat_index['education_num'] ] = education_num
  marital_status = es.pop(0)
  x[ cat_index[marital_status] ] = 1.0
  occupation = es.pop(0)
  x[ cat_index[occupation] ] = 1.0
  relationship = es.pop(0)
  x[ cat_index[relationship] ] = 1.0
  race = es.pop(0)
  x[ cat_index[race] ] = 1.0
  sex = es.pop(0)
  x[ cat_index[sex] ] = 1.0
  capital_gain = float(es.pop(0)) # continuous
  x[ cat_index['capital_gain'] ] = capital_gain
  capital_loss = float(es.pop(0)) # continuous
  x[ cat_index['capital_loss'] ] = capital_loss
  hours_per_week = float(es.pop(0)) # continuous
  x[ cat_index['hours_per_week'] ] = hours_per_week
  native_country = es.pop(0)
  x[ cat_index[native_country] ] = 1.0
  income = es.pop(0)
  print( x )
  y = 1.0 if '>50K' in income else 0.0
  print(y)
  yst.append( y )
  Xst.append( x )
import pickle
open('dataset.pkl', 'wb').write( pickle.dumps( (Xs, ys, Xst, yst) ) )
