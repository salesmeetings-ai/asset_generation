from typing import List, Callable, Dict, Type

from src.domain import VideoClip
from src.domain.video_effects.slice import Slice, apply_slice
from src.domain.video_effects.video_effect import VideoEffect


def apply_effects(video_clip: VideoClip, effects: List[VideoEffect]) -> VideoClip:
    handler_type = Callable[[VideoClip, VideoEffect], VideoClip]
    effects_vs_handlers: Dict[Type[VideoEffect], handler_type] = {
        Slice: apply_slice,
    }
    result_video_clip = video_clip.copy()
    for effect in effects:
        effect_handler: handler_type = effects_vs_handlers[type(effect)]
        result_video_clip = effect_handler(result_video_clip, effect)
    return result_video_clip
