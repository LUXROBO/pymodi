"""AI camera module."""

import cv2 as cv
from typing import Union

class AIcamera(cv2.VideoCapture):

    def __init__(self, source: Union[int, str]):
        super.__init__(source)

    def isOpened(self):
        pass
    def read(self):
        pass
    def show(self):
        pass
    def write(self, frame):
        pass
