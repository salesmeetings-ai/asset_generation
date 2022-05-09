from dataclasses import dataclass
from typing import List

from src.domain import VideoClip
from src.domain.effect import Effect
from src.domain.position import Position


@dataclass
class VideoComponent:
    video_clip: VideoClip
    effects: List[Effect]
