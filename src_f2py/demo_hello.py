import random
import time
import threading
import hello


class SampleThreading(threading.Thread):

    def __init__(self, thread_name):
        self.thread_name = str(thread_name)
        threading.Thread.__init__(self)

    def __str__(self):
        return self.thread_name

    def run(self):
        print('Thread: %s started.' % self)
        sleep_seconds = random.randint(5, 10)
        time.sleep(sleep_seconds)
        print('Thread: %s ended.' % self)


thread_list = []
for i in range(10):
    thread = SampleThreading(thread_name=i)
    thread.start()
    thread_list.append(thread)
    hello.foo(4)

for thread in thread_list:
    thread.join()
