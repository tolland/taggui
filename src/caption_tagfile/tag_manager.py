import json
from pathlib import Path
from typing import Union, Dict, List, Optional

from .caption_tagfile import CaptionTagfile


class TagfileManager:
    @staticmethod
    def get_tagfile_path(image_path: Union[str, Path]) -> Path:
        """Generate the tagfile path (e.g., '.image.jpg.json')."""
        image_path = Path(image_path)
        return image_path.parent / f"{image_path.name}.json"

    @staticmethod
    def get_txt_path(image_path: Union[str, Path]) -> Path:
        image_path = Path(image_path)
        return image_path.parent / f"{image_path.stem}.txt"

    @staticmethod
    def read(image_path: Union[str, Path]) -> CaptionTagfile:
        """Read a tagfile, falling back to .txt if no JSON exists."""
        image_path = Path(image_path)
        tagfile_path = TagfileManager.get_tagfile_path(image_path)
        txt_path = TagfileManager.get_txt_path(image_path)

        # Case 1: JSON exists, load it
        if tagfile_path.exists():
            with open(tagfile_path, "r") as f:
                data = json.load(f)
            return CaptionTagfile(**data)

        # Case 2: No JSON, but .txt exists, migrate to JSON
        if txt_path.exists():
            with open(txt_path, "r") as f:
                txt_caption = f.read().strip()
            tagfile = CaptionTagfile(
                filename=image_path.name,
                captions={"default": txt_caption},
                tags=[]  # No tags in .txt, start empty
            )
            # Write it as JSON for future use
            TagfileManager.write(image_path, tagfile)
            return tagfile

        # Case 3: Neither exists, raise error
        raise FileNotFoundError(f"No tagfile (.json or .txt) found for {image_path}")

    @staticmethod
    def write(image_path: Union[str, Path], tagfile: CaptionTagfile) -> None:
        """Write a CaptionTagfile object to disk as JSON."""
        tagfile_path = TagfileManager.get_tagfile_path(image_path)
        # Update hash if not set
        if not tagfile.hash:
            tagfile.hash = CaptionTagfile.generate_hash(image_path)
        with open(tagfile_path, "w") as f:
            json.dump(tagfile.model_dump(), f, indent=2)

    @staticmethod
    def create(image_path: Union[str, Path], captions: Optional[Dict[str, str]] = None, tags: Optional[List[str]] = None) -> CaptionTagfile:
        """Create a new tagfile, checking for existing .txt."""
        image_path = Path(image_path)
        txt_path = TagfileManager.get_txt_path(image_path)
        captions = captions or {}

        # If .txt exists and no 'default' caption provided, migrate it
        if txt_path.exists() and "default" not in captions:
            with open(txt_path, "r") as f:
                captions["default"] = f.read().strip()

        tagfile = CaptionTagfile(
            filename=image_path.name,
            captions=captions,
            tags=tags or []
        )
        TagfileManager.write(image_path, tagfile)
        return tagfile