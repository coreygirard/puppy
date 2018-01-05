import unittest
import doctest
import puppy


class TestBasic(unittest.TestCase):
    def test_basic(self):
        pupper = puppy.Puppy()

        pub = pupper.Pub('topic1')
        sub = pupper.SubPull('topic1')

        pub.send('hello')
        self.assertEqual(sub.recv(),'hello')
        self.assertEqual(sub.recv(),None)

class TestRecvAll(unittest.TestCase):
    def test_recv_all(self):
        pupper = puppy.Puppy()

        pub = pupper.Pub('topic1')
        sub = pupper.SubPull('topic1')

        pub.send('hello')
        self.assertEqual(sub.recvAll(),['hello'])
        self.assertEqual(sub.recvAll(),[])

        pub.send('world')
        self.assertEqual(sub.recvAll(),['world'])
        self.assertEqual(sub.recvAll(),[])

class TestParenting(unittest.TestCase):
    def test_parenting(self):
        pupper = puppy.Puppy()

        pub = pupper.Pub('topic1')
        subC = pupper.SubPull('topic1')
        subP = pupper.SubPull('')

        pub.send('hello')
        pub.send('world')
        self.assertEqual(subC.recvAll(),['hello','world'])
        self.assertEqual(subP.recvAll(),['hello','world'])
        self.assertEqual(subC.recvAll(),[])
        self.assertEqual(subP.recvAll(),[])

    def test_multiple_children(self):
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
        self.assertEqual(subC1.recvAll(),['hello-1','world-1'])
        self.assertEqual(subC1.recvAll(),[])

        self.assertEqual(subC2.recvAll(),['hello-2','world-2'])
        self.assertEqual(subC2.recvAll(),[])

        self.assertEqual(subP.recvAll(),['hello-1','world-1','hello-2','world-2'])
        self.assertEqual(subP.recvAll(),[])




class TestMultiplePublishers(unittest.TestCase):
    def test_multiplePublishers(self):
        pupper = puppy.Puppy()

        pub1 = pupper.Pub('topic1')
        pub2 = pupper.Pub('topic1')
        sub = pupper.SubPull('topic1')

        pub1.send('hello')
        pub2.send('world')
        self.assertEqual(sub.recvAll(),['hello','world'])
        self.assertEqual(sub.recvAll(),[])

class TestMultipleSubscribers(unittest.TestCase):
    def test_multipleSubscribers(self):
        pupper = puppy.Puppy()

        pub = pupper.Pub('topic1')
        sub1 = pupper.SubPull('topic1')
        sub2 = pupper.SubPull('topic1')

        pub.send('hello')
        self.assertEqual(sub1.recvAll(),['hello'])
        self.assertEqual(sub1.recvAll(),[])

        self.assertEqual(sub2.recvAll(),['hello'])
        self.assertEqual(sub2.recvAll(),[])


class Latch(object):
    def __init__(self):
        self.value = None

    def set(self,e):
        self.value = e

class TestPushSubscribe(unittest.TestCase):
    def test_push_subscribe(self):
        pupper = puppy.Puppy()

        latch = Latch()

        pub = pupper.Pub('topic1')

        pupper.SubPush('topic1',latch.set)

        self.assertEqual(latch.value,None)
        pub.send('hello')
        self.assertEqual(latch.value,'hello')
        pub.send('world')
        self.assertEqual(latch.value,'world')

class TestFilter(unittest.TestCase):
    def test_filter(self):
        pupper = puppy.Puppy()

        pub = pupper.Pub('topic1')

        sub = pupper.SubPull('topic1',
                             filter=lambda i : i[2] == 'c')

        pub.send('ab')
        pub.send('abc')
        pub.send('abd')
        pub.send('abcd')
        self.assertEqual(sub.recvAll(),['abc','abcd'])


class TestVerify(unittest.TestCase):
    def test_verify(self):
        pupper = puppy.Puppy()
        pupper.verify()



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(puppy))
    return tests

if __name__ == '__main__':
    unittest.main()
