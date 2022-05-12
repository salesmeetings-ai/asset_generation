from dataclasses import dataclass
from typing import List

from src.domain import VideoClip
from src.domain.effects import Effect, apply_effects


@dataclass
class VideoComponent:
    video_clip: VideoClip
    effects: List[Effect]

    def get_video_clip_with_effects(self):
        result_video_clip = self.video_clip.copy()
        return apply_effects(result_video_clip, self.effects)
