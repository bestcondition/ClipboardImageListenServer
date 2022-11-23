import time
from typing import Callable, Any, Optional
from PIL.Image import Image
from PIL.ImageGrab import grabclipboard
from loguru import logger


class ClipboardImageListenServer:
    def __init__(self, heartbeat_second: float, new_image_callback: Callable[[Image], Any]):
        # how many second check the clipboard
        self.heartbeat_second = heartbeat_second
        # callback function for new image come from clipboard
        self.new_image_callback = new_image_callback

        self.last_image: Optional[Image] = None
    
    def server_forever(self):
        while True:
            self.listen_once()
            time.sleep(self.heartbeat_second)
    
    def listen_once(self):
        try:
            may_new_image = grabclipboard()
        except Exception as e:
            may_new_image = None
        if may_new_image is not None:
            if self.last_image is None or not self.image_eq(self.last_image, may_new_image):
                self.last_image = may_new_image
                logger.info(f'new image from clipboard')
                self.new_image_callback(may_new_image)
    
    @staticmethod
    def image_eq(image1: Image, image2: Image):
        return image1.tobytes() == image2.tobytes()
