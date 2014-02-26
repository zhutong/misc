#encoding=utf-8
import threading
import time
from Queue import Queue

class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            for i in range(100):
                if queue.qsize() > 500:
                     pass
                else:
                     count = count +1
                     msg = self.name + '生成产品'+str(count)
                     queue.put(msg)
                     print msg
            time.sleep(1)

class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            for i in range(3):
                if queue.qsize() < 100:
                    pass
                else:
                    msg = self.name + '消费了 '+queue.get()
                    print msg
            time.sleep(1)

queue = Queue()


def test():
    for i in range(200):
        queue.put('初始产品'+str(i))
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(5):
        c = Consumer()
        c.start()
if __name__ == '__main__':
    test()