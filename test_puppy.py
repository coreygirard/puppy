import time
from puppy import Puppy

def f(e):
    print(e)

p = Puppy()

pub = p.Pub('topicA')
p.SubPush('topicA',f)
sub = p.SubPull('topicA')

pub.send([1,2,3])

time.sleep(1)
print(sub.recv())
