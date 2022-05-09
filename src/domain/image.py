from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import PIL.Image
import numpy
import requests

from .dimensions import Dimensions
from .position import Position


class Image:
    def __init__(self, image: PIL.Image, position: None or Position = None):
        self.pil_image = image
        self._rendered_image: PIL.Image = None
        if position is None:
            position = Position(0, 0)
        self.position = position
        self._children: List[Image] = []

    @classmethod
    def from_url(cls, url: str, **kwargs):
        image = PIL.Image.open(requests.get(url, stream=True).raw)
        image = image.convert("RGBA")
        return cls(image, **kwargs)

    @classmethod
    def from_path(cls, path: Path, **kwargs):
        image = PIL.Image.open(str(path))
        image = image.convert("RGBA")
        return cls(image, **kwargs)

    def resize(self, dimensions: Dimensions):
        self.pil_image = self.pil_image.resize(dimensions.width_height_tuple())

    def get_dimensions(self):
        width_height_tuple = self.pil_image.size
        return Dimensions.from_width_height_tuple(width_height_tuple)

    def get_height_to_width_ratio(self) -> float:
        dimensions = self.get_dimensions()
        return dimensions.height / dimensions.width

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.render()
        self._rendered_image.save(str(path))

    def get_as_numpy_array(self):
        self.render()
        return numpy.array(self._rendered_image)

    def add(self, image: "Image"):
        if self is image:
            raise ValueError("Cannot add image to itself!")
        self._children.append(image)

    def add_all(self, images: List["Image"]):
        for image in images:
            self.add(image)

    def render(self):
        self._rendered_image = self.pil_image
        for child in self._children:
            self._consolidate_rendered_image_with_child(child)
        return self._rendered_image

    def _consolidate_rendered_image_with_child(self, child: "Image"):
        child.render()
        (
            horizontal_displacement,
            vertical_displacement,
        ) = child.position.horizontal_vertical_tuple()
        self._rendered_image.paste(
            child.pil_image,
            box=[horizontal_displacement, vertical_displacement],
            mask=child.pil_image,
        )

    def bytes(self):
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "image.png"
            self.save(file_path)
            with open(file_path, "rb") as bytes_file:
                return bytes_file.read()
