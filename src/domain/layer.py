from dataclasses import dataclass
from typing import List

from src.domain.video_effects import VideoEffect, apply_effects
from src.domain.video_clip import (
    concatenate_video_clips,
    VideoClip,
    compose_video_clips,
)
from src.domain.video_component import VideoComponent


@dataclass
class Layer:
    depth: int
    video_components: List[VideoComponent]
    effects: List[VideoEffect]

    def get_layer_video(self):
        layer_video_clip = concatenate_video_clips(
            [
                video_component.get_video_clip_with_effects()
                for video_component in self.video_components
            ]
        )
        return apply_effects(layer_video_clip, self.effects)


def compose_layers(layers: List[Layer]) -> VideoClip:
    sorted_layers = sorted(layers, key=lambda layer: layer.depth, reverse=True)
    sorted_layer_videos = [layer.get_layer_video() for layer in sorted_layers]
    return compose_video_clips(sorted_layer_videos)
