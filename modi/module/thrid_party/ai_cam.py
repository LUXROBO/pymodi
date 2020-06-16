"""AI camera module."""

import cv2
from typing import Union
from modi.util.conn_util import is_modi_pi, AIModuleNotFoundException

if is_modi_pi():
    import usb.core

class AIcamera():

    def __init__(self, source: Union[int, str]):
        if not self.is_ai_cam_connected():
            raise AIModuleNotFoundException("Cannot find MODI AI Camera")

        self.cap = cv2.VideoCapture(source)
        # init video codec for raspberry pi 
        self.fourcc = cv2.VideoWriter_fourcc(*"MPV4")

    def is_ai_cam_connected():
        ai_cam_id_vendor = 0x0c45
        ai_cam_id_product = 0x62c0

        dev = usb.core.find(
            idVendor=ai_cam_id_vendor,
            idProduct=ai_cam_id_product)

        if dev is None:
            return False        
        else:
            return True

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
