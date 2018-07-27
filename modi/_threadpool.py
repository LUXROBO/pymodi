import sys
IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty

import threading
from threading import Thread


class Worker(Thread):
    _TIMEOUT = 2
    """ Thread executing tasks from a given tasks queue. Thread is signalable, 
        to exit
    """
    def __init__(self, tasks, th_num):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon, self.th_num = True, th_num
        self.done = threading.Event()
        self.start()

    def run(self):       
        while not self.done.is_set():
            try:
                func, args, kwargs = self.tasks.get(block=True,
                                                   timeout=self._TIMEOUT)
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(e)
                finally:
                    self.tasks.task_done()
            except Empty as e:
                pass
        return

    def signal_exit(self):
        """ Signal to thread to exit """
        self.done.set()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads, tasks=[]):
        self.tasks = Queue(num_threads)
        self.workers = []
        self.done = False
        self._init_workers(num_threads)
        for task in tasks:
            self.tasks.put(task)

    def _init_workers(self, num_threads):
        for i in range(num_threads):
            self.workers.append(Worker(self.tasks, i))

    def add_task(self, func, *args, **kwargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kwargs))

    def _close_all_threads(self):
        """ Signal all threads to exit and lose the references to them """
        for workr in self.workers:
            workr.signal_exit()
        self.workers = []

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

    def __del__(self):
        self._close_all_threads()


def create_task(func, *args, **kwargs):
    return (func, args, kwargs)