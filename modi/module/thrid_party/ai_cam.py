"""AI camera module."""

import cv2
from typing import Union

class AIcamera():

    def __init__(self, source: Union[int, str]):
        self.cap = cv2.VideoCapture(source)

    def isOpened(self):
        return self.cap.isOpened()
        
    def read(self):
        _, self.frame = self.cap.read()

        self.frame = cv2.flip(self.frame, 1)

        return self.frame

    def show(self):
        pass
    def write(self, frame):
        pass
