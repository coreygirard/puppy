import queue
import time
import threading


class Publisher(object):
    def __init__(self,puppy,topic):
        self.puppy = puppy
        self.topic = topic

    def send(self,data):
        self.puppy.inject(self.topic,data)

class SubscriberPush(object):
    def __init__(self,f):
        self.f = f

    def send(self,data):
        self.f(data)

class SubscriberPull(object):
    def __init__(self):
        self.q = queue.Queue()

    def send(self,data):
        self.q.put(data)

    def recv(self):
        try:
            return self.q.get(block=False)
        except:
            return None

class Topic(object):
    def __init__(self,name):
        self.name = name
        self.sub = []

    def send(self,data):
        #print("Topic '{0}' received: {1}".format(self.name,data))
        for s in self.sub:
            s.send(data)

    def addSubPush(self,f):
        self.sub.append(SubscriberPush(f))

    def addSubPull(self,s):
        self.sub.append(s)

class Puppy(object):
    def __init__(self):
        self.topic = {}

    def Pub(self,topic):
        if type(topic) != type([]):
            topic = [topic]

        for t in topic:
            if t not in self.topic.keys():
                self.topic[t] = Topic(t)

        return Publisher(self,topic)

    def SubPush(self,topic,f):
        if type(topic) != type([]):
            topic = [topic]

        for t in topic:
            self.topic[t].addSubPush(f)

    def SubPull(self,topic):
        if type(topic) != type([]):
            topic = [topic]

        s = SubscriberPull()
        for t in topic:
            self.topic[t].addSubPull(s)

        return s

    def inject(self,topic,data):
        if type(topic) != type([]):
            topic = [topic]

        for t in topic:
            assert(type(t) == str)
            self.topic[t].send(data)

    def verify(self):
        # check that all topics have both publishers and subscribers
        pass


def f(data):
    print("'f' received: {0}".format(repr(data)))

def g(data):
    print("'g' received: {0}".format(repr(data)))

def h(data):
    print("'h' received: {0}".format(repr(data)))

puppy = Puppy()
pub1 = puppy.Pub(['topic1','topic2'])

puppy.SubPush('topic1',f)
sub1 = puppy.SubPull('topic2')

pub1.send([1,2])

print(sub1.recv())
print(sub1.recv())





'''

class Puppy(object):
    def __init__(self,kill=None):
        self.toPuppy = queue.Queue()

        if not kill:
            self.kill = lambda i : i[0] == 'kill'
        else:
            self.kill = kill

        self.q = {}

        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = False#True

    def Pub(self,topic):
        return Publisher()

    def register(self,name,sub,f,topic='.'):
        # TODO: support topics

        assert(name not in self.q.keys())

        d = {}
        d['queue'] = queue.Queue()
        d['func'] = f
        d['thread'] = threading.Thread(target=sub,
                                       args=(d['queue'],
                                             self.toPuppy))
        d['thread'].daemon = True
        d['thread'].start()


        self.q[name] = d

    def start(self):
        self.thread.start()

    def inject(self,data):
        self.toPuppy.put(data)

    def loop(self):
        while True:
            item = self.toPuppy.get()

            try:
                if self.kill(item):
                    break
            except:
                pass

            for v in self.q.values():
                try:
                    if v['func'](item):
                        v['queue'].put(item)
                except:
                    pass
'''
