from dataclasses import dataclass

from src.domain import VideoClip
from src.domain.video_effects.video_effect import VideoEffect


@dataclass
class Slice(VideoEffect):
    time_start: float
    time_end: float


def apply_slice(video_clip: VideoClip, slice: Slice) -> VideoClip:
    video_clip = video_clip.copy()
    return video_clip.get_subclip(slice.time_start, slice.time_end)
