__author__ = 'zhutong'


#!/usr/bin/env python
import Queue
import threading
import time
import random

q = Queue.Queue(0)
NUM_WORKERS = 3


class MyThread(threading.Thread):
    """A worker thread."""

    def __init__(self, input, worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)

    def run(self):
        """
        Get a job and process it.
        Stop when there's no more jobs
        """
        while True:
            if self._jobq.qsize() > 0:
                job = self._jobq.get()
                worktype = self._work_type
                self._process_job(job, worktype)
            else:
                break

    def _process_job(self, job, worktype):
        """
        Do useful work here.
        worktype: let this thread do different work
        1,do list
        2,do item
        3,,,
        """
        doJob(job)


def doJob(job):
    """
    do work function 1
    """
    time.sleep(random.random() * 3)
    print "doing ", job


if __name__ == '__main__':

    print "begin..."
    #put some work to q
    for i in range(NUM_WORKERS * 2):
        q.put(i)
    #print total job q's size
    print "job q'size", q.qsize()
    #start threads to work
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
        #if q is not empty, wait
        while q.qsize() > 0:
            time.sleep(0.1)