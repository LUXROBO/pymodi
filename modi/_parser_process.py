import multiprocessing

from modi._parser_task import ParserTask


class ParserProcess(multiprocessing.Process):
    """
    :param queue serial_read_q: Multiprocessing Queue for serial reading data
    :param queue json_recv_q: Multiprocessing Queue for json message
    """

    def __init__(self, serial_read_q, json_recv_q):
        super(ParserProcess, self).__init__()
        self.__par_task = ParserTask(serial_read_q, json_recv_q)
        self.__stop = multiprocessing.Event()

    def run(self):
        """ Run parser task
        """

        while not self.stopped():
            self.__par_task.run()

    def stop(self):
        """ Stop parser task
        """

        self.__stop.set()

    def stopped(self):
        """ Check parser task status
        """

        return self.__stop.is_set()
