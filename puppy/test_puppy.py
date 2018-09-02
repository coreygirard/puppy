import time
import puppy


def test_basic():
    pupper = puppy.Puppy()

    pub = pupper.Pub('topic1')
    sub = pupper.SubPull('topic1')

    pub.send('hello')
    time.sleep(0.1)
    assert sub.recv() == 'hello'
    assert sub.recv() is None


def test_recv_all():
    pupper = puppy.Puppy()

    pub = pupper.Pub('topic1')
    sub = pupper.SubPull('topic1')

    pub.send('hello')
    time.sleep(0.1)
    assert sub.recv_all() == ['hello']
    assert sub.recv_all() == []

    pub.send('world')
    time.sleep(0.1)
    assert sub.recv_all() == ['world']
    assert sub.recv_all() == []


def test_parenting():
    pupper = puppy.Puppy()

    pub = pupper.Pub('topic1')
    subC = pupper.SubPull('topic1')
    subP = pupper.SubPull('')

    pub.send('hello')
    pub.send('world')
    time.sleep(0.1)
    assert subC.recv_all() == ['hello', 'world']
    assert subP.recv_all() == ['hello', 'world']
    assert subC.recv_all() == []
    assert subP.recv_all() == []

def test_multiple_children():
    pupper = puppy.Puppy()

    pub1 = pupper.Pub('topic1')
    pub2 = pupper.Pub('topic2')

    subC1 = pupper.SubPull('topic1')
    subC2 = pupper.SubPull('topic2')
    subP = pupper.SubPull('')

    pub1.send('hello-1')
    pub1.send('world-1')
    pub2.send('hello-2')
    pub2.send('world-2')
    time.sleep(0.1)
    assert subC1.recv_all() == ['hello-1', 'world-1']
    assert subC1.recv_all() == []

    assert subC2.recv_all() == ['hello-2', 'world-2']
    assert subC2.recv_all() == []

    assert subP.recv_all() == ['hello-1', 'world-1', 'hello-2', 'world-2']
    assert subP.recv_all() == []


def test_multiplePublishers():
    pupper = puppy.Puppy()

    pub1 = pupper.Pub('topic1')
    pub2 = pupper.Pub('topic1')
    sub = pupper.SubPull('topic1')

    pub1.send('hello')
    pub2.send('world')
    time.sleep(0.1)
    assert sub.recv_all() == ['hello', 'world']
    assert sub.recv_all() == []

def test_multipleSubscribers():
    pupper = puppy.Puppy()

    pub = pupper.Pub('topic1')
    sub1 = pupper.SubPull('topic1')
    sub2 = pupper.SubPull('topic1')

    pub.send('hello')
    time.sleep(0.1)

    assert sub1.recv_all() == ['hello']
    assert sub1.recv_all() == []

    assert sub2.recv_all() == ['hello']
    assert sub2.recv_all() == []


class Latch(object):
    def __init__(self):
        self.value = None

    def set(self, e):
        self.value = e


def test_push_subscribe():
    pupper = puppy.Puppy()

    latch = Latch()

    pub = pupper.Pub('topic1')

    pupper.SubPush('topic1', latch.set)

    assert latch.value == None
    pub.send('hello')
    time.sleep(0.1)
    assert latch.value == 'hello'
    pub.send('world')
    time.sleep(0.1)
    assert latch.value == 'world'

def test_filter():
    pupper = puppy.Puppy()

    pub = pupper.Pub('topic1')

    sub = pupper.SubPull('topic1',
                         filter=lambda i: i[2] == 'c')

    pub.send('ab')
    pub.send('abc')
    pub.send('abd')
    pub.send('abcd')
    time.sleep(0.1)
    assert sub.recv_all() == ['abc', 'abcd']


def test_verify():
    pupper = puppy.Puppy()
    pupper.verify()
