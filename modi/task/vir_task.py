
from modi.task.conn_task import ConnTask


class VirTask(ConnTask):

    def __init__(self, verbose=False):
        pass

    #
    # Inherited Methods
    #
    def open_conn(self):
        pass

    def close_conn(self):
        pass

    @ConnTask.wait
    def send(self, pkt):
        pass

    def send_nowait(self, pkt):
        pass

    def recv(self):
        pass