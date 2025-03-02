from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtGui import QIcon



@dataclass
class ImageTags:
    model: str = "default"
    tags: list[str] = field(default_factory=list)

@dataclass
class Image:
    path: Path
    dimensions: tuple[int, int] | None
    tags: ImageTags = field(default_factory=ImageTags)
    tags_model: str | None = None
    thumbnail: QIcon | None = None
