from pathlib import Path
from itertools import count
from typing import Iterator

from PIL.Image import Image
from loguru import logger

from clipboard_image_listen import ClipboardImageListenServer


class ImageSaveFromClipboardServer:
    def __init__(self, file_name_gen: Iterator[str]):
        self.file_name_gen = file_name_gen
    
    def new_image_callback(self, image: Image):
        new_filename = next(self.file_name_gen)
        image.save(new_filename)
        logger.info(f'new image save to --> {new_filename}')
    
    def run(self, heartbeat_second):
        listener = ClipboardImageListenServer(
            heartbeat_second=heartbeat_second,
            new_image_callback=self.new_image_callback
        )
        logger.info('server begin')
        listener.server_forever()


def number_increase_image_save(folder):
    folder_path = Path(folder)
    server = ImageSaveFromClipboardServer(
        str(folder_path.joinpath(f'{i + 1}.png').absolute())
        for i in count()
    )
    server.run(heartbeat_second=.5)


def main():
    number_increase_image_save(r'C:\Users\bestcondition\Documents\test')


if __name__ == '__main__':
    main()
