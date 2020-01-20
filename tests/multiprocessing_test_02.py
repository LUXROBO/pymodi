import multiprocessing
import threading
import time
import os

class MyProcess(multiprocessing.Process):

    #def __init__(self, **kwargs):
    def __init__(self):
        #super(MyProcess, self).__init__(**kwargs)
        super(MyProcess, self).__init__()
        self.dostuff = DoStuff(self)

    def run(self):
        print("MyProcess.run()")
        print("MyProcess.ident = " + repr(self.ident))
        if os.name == 'nt':
            self.dostuff.start_thread()

class DoStuff(object):
    #def __init__(self, owner, **kwargs):
    def __init__(self, owner):
        #super(DoStuff, self).__init__(**kwargs)
        super(DoStuff, self).__init__()
        self.owner = owner
        if os.name != 'nt':
            self.start_thread()

    def start_thread(self):
        print("DoStuff.start_thread()")
        self.my_thread_instance = MyThread(self)
        self.my_thread_instance.start()
        time.sleep(0.1)

class MyThread(threading.Thread):
    def __init__(self, owner):
        super(MyThread, self).__init__()
        self.owner = owner

    def run(self):
        print("MyThread.run()")
        print("MyThread.ident = " + repr(self.ident))
        print("MyThread.owner.owner.ident = " + repr(self.owner.owner.ident))

if __name__ == '__main__':
    mp_target = MyProcess()       # Also pass the pipe to transfer data
    mp_target.daemon = True
    mp_target.start()
    time.sleep(0.1)