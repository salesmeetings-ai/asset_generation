from typing import List, Dict

from src.domain import VideoClip
from src.domain.video_clip import concatenate_video_clips
from src.domain.video_component import VideoComponent


class VideoComponentsCompositor:
    def __init__(self, layers: Dict[int, List[VideoComponent]]):
        self._layers = layers

    def compose(self) -> VideoClip:
        layers_vs_videos = {}
        for layer_number, video_components in self._layers:
            layers_vs_videos[layer_number] = self._get_layer_video(video_components)
        return self._set_duration_and_overlay_layers_videos(layers_vs_videos)

    def _get_layer_video(self, video_components: List[VideoComponent]) -> VideoClip:
        return concatenate_video_clips(
            [
                self._get_video_with_effects_applied(video_component)
                for video_component in video_components
            ]
        )

    @staticmethod
    def _get_video_with_effects_applied(video_component: VideoComponent) -> VideoClip:
        result_video_clip = video_component.video_clip.copy()
        for effect in video_component.effects:
            result_video_clip.apply_effect(effect)
        return result_video_clip

    @staticmethod
    def _set_duration_and_overlay_layers_videos(
        layers_vs_videos: Dict[int, VideoClip]
    ) -> VideoClip:
        sorted_layer_keys = sorted(layers_vs_videos.keys(), reverse=True)
        sorted_video_clips = [layers_vs_videos[key] for key in sorted_layer_keys]
        max_duration = max([video_clip.duration for video_clip in sorted_video_clips])
        for i in range(len(sorted_video_clips)):
            sorted_video_clips[i].duration = max_duration
        result_video_clip = sorted_video_clips[0].copy()
        for video_clip in sorted_video_clips[1:]:
            result_video_clip.add_overlay(video_clip)
        return result_video_clip
