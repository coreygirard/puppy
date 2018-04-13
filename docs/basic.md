# Basic usage

### Publishers

`Publishers` are created by calling `.Pub()` on the `Puppy` object. A `topics` argument is passed, either a string or list of strings, specifying which topics the `Publisher` should publish to:

```python
import puppy as pup

puppy = pup.Puppy()

pub1 = puppy.Pub('topic1')
pub2 = puppy.Pub(['topic1', 'topic2'])

```

### Subscribers (Push)

To register a push subscriber, call `.SubPush()` on the `Puppy` object, with two arguments. The first is the `topics` argument, either a string or list of strings, specifying which topics the `Subscriber` should be subscribed to. The second is a callback function that is called for each message published to each of the subscribed topics.

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub('topic1')


def exampleSubscriber(data):
    print('Subscriber received: {0}'.format(repr(data))

puppy.SubPush('topic1', exampleSubscriber)

pub.send('hello')
```
```
Subscriber received: 'hello'
```

It's important to note that the function is called once for each message on each topic, regardless of the message origin:

```python
import puppy as pup

puppy = pup.Puppy()
pub = puppy.Pub(['topic1', 'topic2'])


def exampleSubscriber(data):
    print('Subscriber received: {0}'.format(repr(data))

puppy.SubPush(['topic1', 'topic2'],exampleSubscriber)

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

- `.recv_all()` is a non-blocking query that:
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
print(sub2.recv_all())

pub.send('hello')
pub.send('world')

print(sub1.recv())
print(sub1.recv())
print(sub1.recv())

print(sub2.recv_all())
print(sub2.recv_all())
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
