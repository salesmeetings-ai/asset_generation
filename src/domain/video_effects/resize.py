from dataclasses import dataclass

from src.domain import VideoClip
from src.domain.dimensions import Dimensions


@dataclass
class Resize:
    dimensions: Dimensions


def apply_resize(video_clip: VideoClip, resize: Resize) -> VideoClip:
    video_clip = video_clip.copy()
    return video_clip.resize(resize.dimensions)
