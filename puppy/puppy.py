import time
import threading
from pprint import pprint

try:
    import queue
except ImportError:
    import Queue as queue

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

    def recvAll(self):
        resp = []
        while True:
            e = self.recv()
            if e == None:
                break
            else:
                resp.append(e)
        return resp


class Topic(object):
    def __init__(self,name,parent=None):
        self.name = name
        self.sub = []
        self.parent = parent

    def send(self,data):
        #print("Topic '{0}' received: {1}".format(self.name,data))
        for s,f in self.sub:
            if f != None:
                try:
                    if f(data) == False:
                        continue
                except:
                    continue

            t = threading.Thread(target=s.send,
                                 args=(data,))
            t.daemon = False
            t.start()
            t = None

        if self.parent:
            self.parent.send(data)

    def addSubPush(self,f,filter=None):
        self.sub.append((SubscriberPush(f),filter))

    def addSubPull(self,s,filter=None):
        self.sub.append((s,filter))

def sanitizeTopics(topic,delim):
    '''
    >>> sanitizeTopics(['aaa','aaa/bbb','aaa/bbb/ccc'],'/')
    ['aaa', 'aaa/bbb', 'aaa/bbb/ccc']

    >>> sanitizeTopics(['aaa','aaa/','/aaa/','/aaa/bbb/'],'/')
    ['aaa', 'aaa', 'aaa', 'aaa/bbb']

    >>> sanitizeTopics(['aaa','aaa/bbb','aaa/bbb/ccc'],'/')
    ['aaa', 'aaa/bbb', 'aaa/bbb/ccc']
    '''

    if type(topic) != type([]):
        topic = [topic]

    return [e.strip(delim) for e in topic]

def getParentChild(topic,delim):
    '''
    >>> pc = getParentChild('aaa/bbb/ccc','/')
    >>> pc == [('', 'aaa'),
    ...        ('aaa', 'aaa/bbb'),
    ...        ('aaa/bbb', 'aaa/bbb/ccc')]
    True

    >>> getParentChild('aaa','/')
    [('', 'aaa')]
    '''

    t = [e for e in topic.split(delim) if e != '']

    temp = []
    for i in range(len(t)):
        temp.append((delim.join(t[:i]),
                     delim.join(t[:i+1])))

    return temp

class Puppy(object):
    def __init__(self,delim='/'):
        self.delim = delim # TODO: implement subtopics: 'aaa/bbb/ccc', etc

        self.topic = {'':Topic('')}

    def Pub(self,topics):
        topics = sanitizeTopics(topics,self.delim)

        for t in topics:
            for a,b in getParentChild(t,self.delim):
                if b not in self.topic.keys():
                    self.topic[b] = Topic(name=b,
                                          parent=self.topic[a])

        return Publisher(self,topics)

    def SubPush(self,topics,f,filter=None):
        topics = sanitizeTopics(topics,self.delim)

        for t in topics:
            self.topic[t].addSubPush(f,filter)

    def SubPull(self,topics,filter=None):
        topics = sanitizeTopics(topics,self.delim)

        s = SubscriberPull()
        for t in topics:
            self.topic[t].addSubPull(s,filter)

        return s

    def inject(self,topics,data):
        topics = sanitizeTopics(topics,self.delim)

        for t in topics:
            assert(type(t) == str)
            self.topic[t].send(data)

    def verify(self):
        # check that all topics have both publishers and subscribers
        pass
