from dataclasses import dataclass

from src.domain import Image, VideoClip

@dataclass
class CircleMask:
    image: Image
    time_start: float
    duration: float


def apply_circle_mask(video_clip: VideoClip, circle_mask: CircleMask) -> VideoClip:
    pass
