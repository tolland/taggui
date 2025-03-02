from abc import ABC, abstractmethod
from pathlib import Path

from caption_tagfile.tag_manager import TagfileManager
from utils.image import Image, ImageTags
from PySide6.QtWidgets import QMessageBox


class BaseIoProvider(ABC):
    """
    Abstract base class for reading and writing tags.

    This class defines the interface for tag management and includes
    common functionality that can be shared across different implementations.
    """

    @staticmethod
    @abstractmethod
    def read_image_tags(path: Path | str, tag_separator: str) -> ImageTags:
        """
        Retrieves tags for image file
        """
        pass

    @staticmethod
    @abstractmethod
    def write_image_tags(image: Image, tag_separator: str):
        """
        Retrieves tags for image file
        """
        pass


class TxtFileIoProvider(BaseIoProvider):
    """
    Reads and writes tags to a text file in the kohya_ss
    traditional format.
    """

    @staticmethod
    def write_image_tags(image: Image, tag_separator: str):
        print(f"writing image tags to disk for {image.path}")
        try:
            image.path.with_suffix('.txt').write_text(
                tag_separator.join(image.tags.tags), encoding='utf-8',
                errors='replace')
        except OSError:
            error_message_box = QMessageBox()
            error_message_box.setWindowTitle('Error')
            error_message_box.setIcon(QMessageBox.Icon.Critical)
            error_message_box.setText(f'Failed to save tags for {image.path}.')
            error_message_box.exec()
        try:
            mgr = TagfileManager()
            mgr.create(image.path, captions={"test": "hello"}, tags=["tag1"], )
        except OSError:
            print("it didn't bloody work!")

    @staticmethod
    def read_image_tags(path: Path, tag_separator: str):
        # caption = path.read_text(encoding='utf-8',                               errors='replace')
        mgr = TagfileManager()
        loaded = mgr.read(path)
        caption = loaded.captions["default"]
        tags = []
        if caption:
            tags = caption.split(tag_separator)
            tags = [tag.strip() for tag in tags]
            tags = [tag for tag in tags if tag]
        return ImageTags(tags=tags, model="default")
