import os
import time
import threading
import multiprocessing
from multiprocessing import Process, Queue
from multiprocessing import Manager


class DoStuff(object):
    #def __init__(self, owner, **kwargs):
    def __init__(self, owner):
        #super(DoStuff, self).__init__(**kwargs)
        super(DoStuff, self).__init__()
        if os.name != 'nt':
            self.start_thread()

    def start_thread(self):
        while True:
            print('ReadDataProc_Thread.pid():', os.getpid())
            # self.my_thread_instance = MyThread(self)
            # self.my_thread_instance.start()
            time.sleep(0.1)

class DoStuff2(object):
    #def __init__(self, owner, **kwargs):
    def __init__(self, owner):
        #super(DoStuff, self).__init__(**kwargs)
        super(DoStuff2, self).__init__()
        if os.name != 'nt':
            self.start_thread()

    def start_thread(self):
        while True:
            print('ProcDataProc_Thread.pid():', os.getpid())
            # self.my_thread_instance = MyThread(self)
            # self.my_thread_instance.start()
            time.sleep(0.1)

class ReadDataProc(multiprocessing.Process):
    def __init__(self):
        super(ReadDataProc, self).__init__()
        self.dostuff = DoStuff(self)
        print('ReadProcInit')

    def run(self):
        print('ReadDataProc.pid():', os.getpid())
        if os.name == 'nt':
            self.dostuff.start_thread()

class ProcDataProc(multiprocessing.Process):
    def __init__(self):
        super(ProcDataProc, self).__init__()
        self.dostuff2 = DoStuff2(self)
        print('ReadProcInit')

    def run(self):
        print('ProcDataProc.pid():', os.getpid())
        if os.name == 'nt':
            self.dostuff2.start_thread()



if __name__ == '__main__': 

    print('test start')
    print('Main.pid():', os.getpid())
    ## 이렇게는 작동 함
    print('pstart1')
    p = ReadDataProc()
    p.daemon = True
    p.start()

    print('pstart2')
    p = ProcDataProc()
    p.daemon = True
    p.start()
    
    time.sleep(10)

    ## 이렇게는 작동하지 않음
    # pros = list()
    # pros = [
    #     ReadDataProc,
    #     ProcDataProc
    # ]
    # for pro in pros:
    #     p = Process(target = pro)
    #     # p = pro()
    #     p.daemon = True
    #     p.start()
    #     pros.append(p)

    print('test End')

