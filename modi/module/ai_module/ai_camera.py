import cv2
import time

from numpy import ndarray
from PIL import Image
from IPython import display as Idisplay
from io import BytesIO
from typing import List
from usb import core

from modi.util.conn_util import AIModuleFaultsException

class AICamera:
    def __init__(self):
        if not self.is_ai_cam_connected():
            raise AIModuleFaultsException("Cannot find MODI AI Camera! Please connect USB Camera")

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
        """Check if camera connected

        :return: list of connected camera devices
        :rtype: String list
        """
        ai_cam_id_vendor = 0x0c45
        ai_cam_id_product = 0x62c0

        dev = core.find(
            idVendor=ai_cam_id_vendor,
            idProduct=ai_cam_id_product
        )
        return dev

    def is_opened(self) -> bool:
        """Check if camera resource opened

        :return: Ture if camera opened
        :rtype: Bool
        """
        return self.cap.isOpened()

    def set_frame_height(self, height: int) -> None:
        """Set height of returned frame

        :param height: Height of the frame
        :return: None
        """
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def set_frame_weight(self, width: int) -> None:
        """Set width of returned frame

        :param width: Width of the frame
        :return: None
        """
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def read(self) -> ndarray:
        """Returns image frame captured

        :return: Image frame
        :rtype: Numpy array
        """
        self.t1 = time.time()
        try:
            ret, _frame = self.cap.read()
            if ret:
                _frame = cv2.flip(_frame, 1)
                self.frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                return self.frame
            else:
                pass
        except:
            self.cap.release()
            Idisplay.clear_output()
            raise Exception('Stream stopped')

    def show(self, frame: ndarray) -> None:
        """Show each frame in Jupyter notebook shell

        :param frame: Image frame
        :type frame: Numpy array
        :return: None
        """
        try:
            im = self._array_to_image(frame)
            self.t2 = time.time()
            s = f"{int(1 / (self.t2 - self.t1))} FPS"
            self.d.update(im)
            self.d2.update(Idisplay.HTML(s))
        except:
            self.cap.release()
            Idisplay.clear_output()
            print("Stream stopped")
            raise Exception()

    def imwrite(self, path: str, frame: ndarray) -> None:
        """Save captrue image frame to given path

        :param path: File path
        :type path: String
        :param frame: Image frame
        :type frame: Numpy array
        :return: None
        """
        # save captured frame image to path
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, frame)

    def set_window(self) -> None:
        """Decide which image to print first in Jupyter shell

        :return: None
        """
        self.d = Idisplay.display("Window", display_id=1)
        self.d2 = Idisplay.display("Frame Rate", display_id=2)

    # Use 'jpeg' instead of 'png' (~5 times faster)
    def _array_to_image(self, frame: ndarray, format: str = 'jpeg') -> None:
        """Convert numpy array frame to image file

        :param frame: Image frame
        :type frame: Numpy array
        :param format: Saved image file type
        :return: String
        """
        try:
            # Create binary stream object
            f = BytesIO()
            # Convert array to binary stream object
            Image.fromarray(frame).save(f, format)
            return Idisplay.Image(data=f.getvalue())
        except:
            raise Exception()
