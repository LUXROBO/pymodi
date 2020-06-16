"""AI camera module."""

import cv2
from typing import Union
from modi.util.conn_util import is_modi_pi, AIModuleNotFoundException
import time
import PIL.Image
from io import BytesIO
import IPython.display

if is_modi_pi():
    import usb.core

class AIcamera():

    def __init__(self, source: Union[int, str]):
        if not self.is_ai_cam_connected():
            raise AIModuleNotFoundException("Cannot find MODI AI Camera")

        self.cap = cv2.VideoCapture(source)
        # init video codec for raspberry pi
        self.fourcc = cv2.VideoWriter_fourcc(*"MPV4")
        # set camera resolution
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        # initialize time point for calculate Frame Rate
        self.t1 = time.time()
        self.t2 = time.time()

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

    def show(self, frame):
        try:
            im = self.array_to_image(frame)
            self.t2 = time.time()
            s = f"""{int(1 / (self.t2 - self.t1))} FPS"""
            self.d.update(im)
            self.d2.update(IPython.display.HTML(s))

        except:
            self.cap.release()
            IPython.display.clear_output()
            print("Stream stopped")
            raise Exception()

    def imwrite(self, path, frame):
        # save captured frame image to path
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, frame)

    def setWindow(self):
        self.d = IPython.display.display("Window", display_id=1)
        self.d2 = IPython.display.display("Frame Rate", display_id=2)

    # Use 'jpeg' instead of 'png' (~5 times faster)
    def array_to_image(self, a, fmt='jpeg'):
        try:
            # Create binary stream object
            f = BytesIO()

            # Convert array to binary stream object
            PIL.Image.fromarray(a).save(f, fmt)

            return IPython.display.Image(data=f.getvalue())
        except:
            raise Exception()

def main():
    aicam = AIcamera()
    aicam.setWindow()
    while True:
        try:
            frame = aicam.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # User CV2 Code
            aicam.show(frame)
        except:
            break
    aicam.imwrite('image.jpeg', frame)

if __name__ == "__main__":
    main()
