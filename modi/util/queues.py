from multiprocessing import Queue
import json


class CommunicationQueue:
    """Communication queue is a priority queue styled queue.
    When communicating with modules, there are certain messages that need
    to be processed before others. This queue selects those messages and
    return earlier than other messages.
    """
    def __init__(self):
        self.__priority = Queue()
        self.__ordinary = Queue()

    def put(self, message: str) -> None:
        if self.__check_priority(message):
            self.__priority.put(message)
        else:
            self.__ordinary.put(message)

    def get(self) -> str:
        if not self.__priority.empty():
            return self.__priority.get()
        else:
            return self.__ordinary.get()

    def get_nowait(self) -> str:
        if not self.__priority.empty():
            return self.__priority.get_nowait()
        else:
            return self.__ordinary.get_nowait()

    @staticmethod
    def __check_priority(json_message: str) -> bool:
        """Checks whether the message has priority

        :param json_message: Json serialized message
        :type json_message: str
        :return: True is the message has priority
        :rtype: bool
        """
        try:
            message = json.loads(json_message)
        except json.JSONDecodeError:
            return False
        command = message['c']
        return command in (0x04, 0x1F, 0x05, 0x09)
