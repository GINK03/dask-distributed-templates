from distributed import Client

client = Client('192.168.14.13:8786')

def inc(x):
  for i in range(10000000):
    x += i
  return x

L = client.map(inc, range(1000))

ga = client.gather(L)
print(ga)
