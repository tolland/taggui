import hashlib
from datetime import UTC, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, field_serializer
from pydantic import Field


class CaptionTagfile(BaseModel):
    filename: str = Field(..., description="Name of the associated image file")
    captions: Dict[str, str] = Field(
        default_factory=dict,
        description="Captions from different models (e.g., 'default': 'from txt', 'florence': '...')"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Manual or auto-generated tags"
    )
    source: Optional[str] = Field(None, description="URL or origin")
    edited: bool = Field(False, description="Flag if edited")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        description="Creation or last update time"
    )
    hash: Optional[str] = Field(None, description="SHA256 hash of the image")

    @field_serializer('timestamp')
    def serialize_dt(self, dt: datetime, _info):
        return dt.timestamp()

    @classmethod
    def generate_hash(cls, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()