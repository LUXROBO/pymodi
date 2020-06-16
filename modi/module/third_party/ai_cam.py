"""AI camera module."""

import cv2
import time
import PIL.Image
import IPython.display

from io import BytesIO
from typing import List

from modi.util.conn_util import is_modi_pi, AIModuleNotFoundException

if is_modi_pi():
    import usb.core

class AIcamera:

    def __init__(self):
        if not self.is_ai_cam_connected():
            raise AIModuleNotFoundException("Cannot find MODI AI Camera")

        self.cap = cv2.VideoCapture(-1)
        # init video codec for raspberry pi
        self.fourcc = cv2.VideoWriter_fourcc(*"MPV4")
        # set camera resolution
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        # initialize time point for calculate Frame Rate
        self.t1 = time.time()
        self.t2 = time.time()

    def is_ai_cam_connected(self) -> List[str]:
        ai_cam_id_vendor = 0x0c45
        ai_cam_id_product = 0x62c0

        dev = usb.core.find(
                            idVendor=ai_cam_id_vendor,
                            idProduct=ai_cam_id_product
                            )

        return dev

    def isOpened(self) -> bool:
        return self.cap.isOpened()

    def set_frame_height(self, height) -> None:
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def set_frame_weight(self, width) -> None:
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def read(self) -> None:
        try:
            self.t1 = time.time()
            ret, _frame = self.cap.read()
            if ret:
                _frame = cv2.flip(_frame, 1)
                self.frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                return self.frame
            else:
                exit()

        except:
            self.cap.release()
            IPython.display.clear_output()
            raise Exception()
            print("Stream stopped")

    def show(self, frame) -> None:
        try:
            im = self._array_to_image(frame)
            self.t2 = time.time()
            s = f"""{int(1 / (self.t2 - self.t1))} FPS"""
            self.d.update(im)
            self.d2.update(IPython.display.HTML(s))

        except:
            self.cap.release()
            IPython.display.clear_output()
            print("Stream stopped")
            raise Exception()

    def imwrite(self, path, frame) -> None:
        # save captured frame image to path
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, frame)

    def set_window(self) -> None:
        self.d = IPython.display.display("Window", display_id=1)
        self.d2 = IPython.display.display("Frame Rate", display_id=2)

    # Use 'jpeg' instead of 'png' (~5 times faster)
    def _array_to_image(self, a, fmt='jpeg') -> None:
        try:
            # Create binary stream object
            f = BytesIO()

            # Convert array to binary stream object
            PIL.Image.fromarray(a).save(f, fmt)

            return IPython.display.Image(data=f.getvalue())
        except:
            raise Exception()
