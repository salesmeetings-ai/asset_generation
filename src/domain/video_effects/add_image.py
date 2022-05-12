from dataclasses import dataclass

from src.domain import Image, VideoClip


@dataclass
class AddImage:
    image: Image
    time_start: float
    duration: float


def apply_add_image(video_clip: VideoClip, add_image: AddImage) -> VideoClip:
    pass
