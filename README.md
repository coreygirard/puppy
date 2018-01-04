# puppy
A featherweight pub/sub architecture genetically engineered to make your project simpler, not more complicated. And to be adorable.

### What's in a name?

Publisher&#8211;Subscriber + Python &#8594; Pub/Sub + .py &#8594; Pub + py &#8594;  ***puppy***


## Hello World

```python
import puppy as pup

puppy = pup.Puppy()

pub = puppy.Pub('topic1')
sub = puppy.SubPull('topic1')

pub.send('hello')
pub.send('world')

print(sub.recvAll())
```
```
['hello', 'world']
```


For those unfamiliar with the Pub/Sub pattern, [Google](https://cloud.google.com/pubsub/docs/overview) and [Wikipedia](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) have pretty useful overviews.



## Basic

### Publishers

`Publishers` are created by calling `.Pub()` on the `Puppy` object. A `topics` argument is passed, either a string or list of strings, specifying which topics the `Publisher` should publish to:

```python
import puppy as pup

puppy = pup.Puppy()

pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub(['topic1','topic2'])

```

### Subscribers (Push)

To register a push subscriber, call `.SubPush()` on the `Puppy` object, with two arguments. The first is the `topics` argument, either a string or list of strings, specifying which topics the `Subscriber` should be subscribed to. The second is a callback function that is called for each message published to each of the subscribed topics.

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub('topic1')


def exampleSubscriber(data):
    print('Subscriber received: {0}'.format(repr(data))

puppy.SubPush('topic1',exampleSubscriber)

pub.send('hello')
```
```
Subscriber received: 'hello'
```

It's important to note that the function is called once for each message on each topic, regardless of the message origin:

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub(['topic1','topic2'])


def exampleSubscriber(data):
    print('Subscriber received: {0}'.format(repr(data))

puppy.SubPush(['topic1','topic2'],exampleSubscriber)

pub.send('hello')
```
```
Subscriber received: 'hello'   # pub -> topic1 -> exampleSubscriber
Subscriber received: 'hello'   # pub -> topic2 -> exampleSubscriber
```


### Subscribers (Pull)

Sometimes it's useful to have messages wait in the queue until requested. Puppy offers pull subscriptions as well. To register a pull subscriber, call `.SubPull()` on the `Puppy` object, with a `topics` argument. This returns a subscriber object. To check for messages, this object provides two methods:

- `.recv()` is a non-blocking query that: 
  - Returns `None` if no unread messages exist 
  - Returns the oldest unread message if any exist

- `.recvAll()` is a non-blocking query that: 
  - Returns `[]` if no unread messages exist
  - Returns a list of all unread messages if any exist, ordered from oldest to newest. 

Each subscriber has its own message queue, which can be consumed without affecting any other subscribers.

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub('topic1')

sub1 = puppy.SubPull('topic1')
sub2 = puppy.SubPull('topic1')

print(sub1.recv())
print(sub2.recvAll())

pub.send('hello')
pub.send('world')

print(sub1.recv())
print(sub1.recv())
print(sub1.recv())

print(sub2.recvAll())
print(sub2.recvAll())
```
```
None
[]

'hello'
'world'
None

['hello', 'world']
[]
```


## Advanced

### Complex Architectures


```python
import puppy as pup

def s1(data):
    print("subscriber1 received: {0}".format(repr(data)))

def s2(data):
    print("subscriber2 received: {0}".format(repr(data)))

puppy = pup.Puppy()

pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub(['topic2','topic3'])
puppy.SubPush(['topic1','topic2'],s1)
puppy.SubPush('topic3',s2)

pub1.send(1)
pub2.send(2)


```

```
subscriber1 received: 1   # pub1 -> topic1 -> sub1
subscriber1 received: 2   # pub2 -> topic2 -> sub1
subscriber2 received: 2   # pub2 -> topic3 -> sub2
```



### Parent/Child topics

An example is worth a thousand words:

```python
import puppy as pup

puppy = pup.Puppy()
pub1 = puppy.Pub('topic1/subtopic1')
pub2 = puppy.Pub('topic1/subtopic2')

sub1 = puppy.SubPull('topic1/subtopic1')
sub2 = puppy.SubPull('topic1/subtopic2')
sub = puppy.SubPull('topic1')

pub1.send('hello')
pub2.send('world')

print(sub1.recvAll())
print(sub2.recvAll())
print(sub.recvAll())
```
```
['hello']
['world']
['hello', 'world']
```

The default delimiter is `/`, but arbitrary delimiters may be passed when constructing the `Puppy` object, eg, `.Puppy(delim='-')`. Behavior for passed delimiters of length greater than one is currently undefined, and may be quite surprising. 

```python
import puppy as pup

puppy = pup.Puppy(delim='.')
pub = puppy.Pub('topic1.subtopic1')

sub1 = puppy.SubPull('topic1.subtopic1')
sub2 = puppy.SubPull('topic1')
sub3 = puppy.SubPull('')

pub1.send(42)

print(sub1.recvAll())
print(sub2.recvAll())
print(sub3.recvAll())
```
```
42
42
42
```

There is actually a root topic of `''`, which receives every single message from any topic, and can be subscribed to:

```python
import puppy as pup

puppy = pup.Puppy()
pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub('topic2')

sub1 = puppy.SubPull('topic1')
sub2 = puppy.SubPull('topic2')
sub = puppy.SubPull('')

pub1.send('hello')
pub2.send('world')

print(sub1.recvAll())
print(sub2.recvAll())
print(sub.recvAll())
```
```
['hello']
['world']
['hello', 'world']
```

Subscribing to `''` will often be useful for logging, for example.


### Filters

It might be useful to have incoming messages filtered by some arbitrary criteria above and beyond topics:

```python
import puppy as pup

puppy = pup.Puppy()
pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub('topic2')

sub = puppy.SubPull('topic1',
                    filter=lambda i : 'e' in i)

pub1.send('hello')
pub2.send('world')
pub2.send('hey')

print(sub.recvAll())
```
```
['hello', 'hey']
```

The function passed as `filter` will be called on each potential message. If the function returns `True`, the message will be queued for the subscriber. If the function errors or returns any other value, the message will not be queued.

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub('topic1')

sub = puppy.SubPull('topic1',
                    filter=lambda i : i[2] == 'c')

pub.send('ab')    # will cause a silent caught error in filter function
pub.send('abc')
pub.send('abd')   # will return False from filter function
pub.send('abcde')

print(sub.recvAll())
```
```
['abc', 'abcde']
```


Non-lambda functions are of course also usable as filter functions:

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub('topic1')

def f(n):
    if n%3 != 0:
        return False
    
    if n%5 != 0:
        return False
    
    return True

sub = puppy.SubPull('topic1',
                    filter=f)

for n in range(50):
	pub.send(n)

print(sub.recvAll())
```
```
[0, 15, 30, 45]
```

## Examples

Project Euler #1:

```python
import time
import puppy as pup

class Filter(object):
    def __init__(self,puppy):
        # publisher to the 'filtered' topic
        self.pub = puppy.Pub('filtered')

    # will receive push from the 'all' topic    
    def recv(self,n):
        if n%3 == 0:
            self.pub.send(n)
        elif n%5 == 0:
            self.pub.send(n)        


puppy = pup.Puppy()

# raw numbers go into the 'all' topic
pub = puppy.Pub('all')

f = Filter(puppy)
puppy.SubPush('all',f.recv)

# subscribe to the filtered results
result = puppy.SubPull('filtered')

# send some data into the 'all' topic
for n in range(1000):
	pub.send(n)

# make sure everything settles down
time.sleep(1) 

# receive everything from the 'filtered' topic and sum it
print(sum(result.recvAll()))

```


