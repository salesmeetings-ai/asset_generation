from dataclasses import dataclass

from src.domain import VideoClip


@dataclass
class LipSync:
    pass


def apply_lip_sync(video_clip: VideoClip, lip_sync: LipSync) -> VideoClip:
    pass
