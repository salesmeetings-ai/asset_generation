from dataclasses import dataclass

from src.domain import VideoClip
from src.domain.position import Position


@dataclass
class SetPosition:
    position: Position


def apply_set_position(video_clip: VideoClip, set_position: SetPosition) -> VideoClip:
    pass
