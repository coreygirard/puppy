# puppy
A pub/sub architecture genetically engineered to make your project simpler, not more complicated. And to be adorable.


```python
import puppy

def s(data):
    print("subscriber received: {0}".format(repr(data)))

puppy = puppy.Puppy()

pub1 = puppy.Pub('topic1')
sub1 = puppy.SubPush('topic1',s)

pub1.send('hello')


```

```
subscriber received: 'hello'
```

---

```python
import puppy

def s1(data):
    print("subscriber1 received: {0}".format(repr(data)))

def s2(data):
    print("subscriber2 received: {0}".format(repr(data)))

puppy = puppy.Puppy()

pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub('topic2')
sub1 = puppy.SubPush('topic1',s1)
sub2 = puppy.SubPush('topic2',s2)

pub1.send('hello')
pub2.send('world')


```

```
subscriber1 received: 'hello'
subscriber2 received: 'world'
```

---

```python
import puppy

def s1(data):
    print("subscriber1 received: {0}".format(repr(data)))

def s2(data):
    print("subscriber2 received: {0}".format(repr(data)))

puppy = puppy.Puppy()

pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub(['topic2','topic3'])
sub1 = puppy.SubPush(['topic1','topic2'],s1)
sub2 = puppy.SubPush('topic3',s2)

pub1.send(1)
pub2.send(2)


```

```
subscriber1 received: 1   # pub1 -> topic1 -> sub1
subscriber1 received: 2   # pub2 -> topic2 -> sub1
subscriber2 received: 2   # pub2 -> topic3 -> sub2
```

