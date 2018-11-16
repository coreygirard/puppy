import time

from src.main import *


def test__basic():
    pupper = Puppy()

    pub = pupper.Pub("topic1")
    sub = pupper.SubPull("topic1")

    pub.send("hello")
    time.sleep(0.1)
    assert sub.recv() == "hello"
    assert sub.recv() is None


def test__recv_all():
    pupper = Puppy()

    pub = pupper.Pub("topic1")
    sub = pupper.SubPull("topic1")

    pub.send("hello")
    time.sleep(0.1)
    assert sub.recv_all() == ["hello"]
    assert sub.recv_all() == []

    pub.send("world")
    time.sleep(0.1)
    assert sub.recv_all() == ["world"]
    assert sub.recv_all() == []


def test__parenting():
    pupper = Puppy()

    pub = pupper.Pub("topic1")
    subC = pupper.SubPull("topic1")
    subP = pupper.SubPull("")

    pub.send("hello")
    pub.send("world")
    time.sleep(0.1)
    assert subC.recv_all() == ["hello", "world"]
    assert subP.recv_all() == ["hello", "world"]
    assert subC.recv_all() == []
    assert subP.recv_all() == []


def test__multiple_children():
    pupper = Puppy()

    pub1 = pupper.Pub("topic1")
    pub2 = pupper.Pub("topic2")

    subC1 = pupper.SubPull("topic1")
    subC2 = pupper.SubPull("topic2")
    subP = pupper.SubPull("")

    pub1.send("hello-1")
    pub1.send("world-1")
    pub2.send("hello-2")
    pub2.send("world-2")
    time.sleep(0.1)
    assert subC1.recv_all() == ["hello-1", "world-1"]
    assert subC1.recv_all() == []

    assert subC2.recv_all() == ["hello-2", "world-2"]
    assert subC2.recv_all() == []

    assert subP.recv_all() == ["hello-1", "world-1", "hello-2", "world-2"]
    assert subP.recv_all() == []


def test__multiple_publishers():
    pupper = Puppy()

    pub1 = pupper.Pub("topic1")
    pub2 = pupper.Pub("topic1")
    sub = pupper.SubPull("topic1")

    pub1.send("hello")
    pub2.send("world")
    time.sleep(0.1)
    assert sub.recv_all() == ["hello", "world"]
    assert sub.recv_all() == []


def test__multiple_subscribers():
    pupper = Puppy()

    pub = pupper.Pub("topic1")
    sub1 = pupper.SubPull("topic1")
    sub2 = pupper.SubPull("topic1")

    pub.send("hello")
    time.sleep(0.1)

    assert sub1.recv_all() == ["hello"]
    assert sub1.recv_all() == []

    assert sub2.recv_all() == ["hello"]
    assert sub2.recv_all() == []


class Latch(object):
    def __init__(self):
        self.value = None

    def set(self, e):
        self.value = e


def test__push_subscribe():
    pupper = Puppy()

    latch = Latch()

    pub = pupper.Pub("topic1")

    pupper.SubPush("topic1", latch.set)

    assert latch.value == None
    pub.send("hello")
    time.sleep(0.1)
    assert latch.value == "hello"
    pub.send("world")
    time.sleep(0.1)
    assert latch.value == "world"


def test__filter():
    pupper = Puppy()

    pub = pupper.Pub("topic1")

    sub = pupper.SubPull("topic1", filter=lambda i: i[2] == "c")

    pub.send("ab")
    pub.send("abc")
    pub.send("abd")
    pub.send("abcd")
    time.sleep(0.1)
    assert sub.recv_all() == ["abc", "abcd"]


def test__verify():
    pupper = Puppy()
    pupper.verify()
