import threading
from queue import Queue
import time

lock = threading.Lock()

def do_work(item):
    time.sleep(.1)

    with lock:
        print(threading.current_thread().name, item)

def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()
for i in range(4):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

start = time.perf_counter()
for item in range(20):
    q.put(item)

q.join()

print('time:', time.perf_counter() - start)