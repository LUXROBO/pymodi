from multiprocessing import queues, get_context
from typing import Optional, TypeVar


class PriorityQueue(queues.Queue):
    _T = TypeVar('_T')

    def __init__(self):
        super().__init__(ctx=get_context())
        self.__priority = queues.Queue(ctx=get_context())
        self.__priority_length = 0
        self.__length = 0

    def put(self, obj: _T, block: bool = ...,
            timeout: Optional[float] = ..., priority: bool = False) -> None:
        if priority:
            self.__priority.put(obj)
            self.__priority_length += 1
        else:
            super().put(obj)
        self.__length += 1

    def get(self, block: bool = ..., timeout: Optional[float] = ...) -> _T:
        self.__length -= 1
        if self.__priority_length > 0:
            self.__priority_length -= 1
            return self.__priority.get()
        else:
            return super().get()

    @property
    def priority_length(self):
        return self.__priority_length

    @property
    def length(self):
        return self.__length
