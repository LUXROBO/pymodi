"""AI camera module."""

import cv2
from typing import Union

class AIcamera():

    def __init__(self, source: Union[int, str]):
        self.cap = cv2.VideoCapture(source)
        # init video codec for raspberry pi 
        self.fourcc = cv2.VideoWriter_fourcc(*"MPV4")

    def isOpened(self):
        return self.cap.isOpened()

    def set_frame_height(self, height):
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def set_frame_weight(self, width):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def read(self):
        _, _frame = self.cap.read()

        _frame = cv2.flip(_frame, 1)

        self.frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)

        return self.frame

    def show(self):
        pass

    def write(self, frame):
        pass
