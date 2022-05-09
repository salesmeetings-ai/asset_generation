import logging
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Tuple, List

import moviepy
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, afx
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.video.fx.speedx import speedx as speed_up
from moviepy.video.tools.drawing import circle

from domain.audio_clip import AudioClip
from domain.dimensions import Dimensions
from domain.image import Image
from domain.position import Position

from src.domain.effect import Effect

log = logging.getLogger(__name__)


class VideoClip:
    def __init__(self, clip: VideoFileClip):
        self.clip = clip
        self._children = []
        self.fps = clip.fps
        self.fuzz = 1

    @classmethod
    def from_path(cls, path: Path or str):
        clip = VideoFileClip(str(path))
        return cls(clip=clip)

    @classmethod
    def from_image_path(cls, path: Path, fps: float = 60):
        clip = ImageClip(str(path))
        clip = clip.set_fps(fps)
        return cls(clip=clip)

    @property
    def duration(self):
        return self.clip.duration

    @duration.setter
    def duration(self, duration):
        self.clip = self.clip.set_duration(duration)

    @property
    def time_start(self):
        return self.clip.start

    @time_start.setter
    def time_start(self, time_start):
        self.clip = self.clip.set_start(time_start)

    @property
    def time_end(self):
        return self.clip.end

    @time_end.setter
    def time_end(self, time_end):
        self.clip = self.clip.set_end(time_end)

    def get_dimensions(self):
        width_height_tuple = self.clip.size
        return Dimensions.from_width_height_tuple(width_height_tuple)

    def set_position(self, position: Position):
        self.clip = self.clip.set_position(position.horizontal_vertical_tuple())

    def copy(self):
        return VideoClip(self.clip.copy())

    def add_overlay(
        self,
        overlay_video_clip: "VideoClip",
        position: Position = Position(0, 0),
    ):
        overlay_video_clip._compose()
        overlay_video_clip.set_position(position)
        self._children.append(overlay_video_clip.clip)

    def change_speed(self, factor: float = None, final_duration: float = None):
        self._compose()
        if factor is None and final_duration is None:
            raise ValueError(
                "One of parameters 'factor' or 'final_duration' should be specified. "
                "Got 'factor' and 'final_duration' with None values"
            )
        self.clip = speed_up(self.clip, factor=factor, final_duration=final_duration)

    def resize(self, dimensions: Dimensions):
        self._compose()
        clip = resize(self.clip, height=dimensions.height, width=dimensions.width)
        return VideoClip(clip)

    def add_image(self, image: Image, time_start: float, duration: float):
        image_bytes = image.get_as_numpy_array()
        image_clip = moviepy.editor.ImageClip(image_bytes).set_position(
            image.position.horizontal_vertical_tuple()
        )
        image_clip.start = time_start
        image_clip.duration = duration
        self._children.append(image_clip)

    def add_image_for_entire_clip(self, image: Image):
        time_start = 0
        duration = self.clip.duration
        self.add_image(image=image, time_start=time_start, duration=duration)

    def add_circle_mask(
        self, circle_center: Tuple[int, int] = None, radius: int = None
    ):
        self._compose()
        width, height = self.clip.size
        if circle_center is None:
            circle_center = (width / 2, height / 2)
        if radius is None:
            radius = min(width, height) / 2

        self.clip = self.clip.add_mask()
        self.clip.mask.get_frame = lambda x: circle(
            screensize=self.clip.size,
            center=circle_center,
            radius=radius,
            col1=1,
            col2=0,
        )

    def set_audio(self, audio_clip: AudioClip):
        self.clip = self.clip.set_audio(audio_clip.clip)

    def get_subclip(self, time_start: float, time_end: float):
        self._compose()
        return VideoClip(self.clip.subclip(t_start=time_start, t_end=time_end))

    def crop(self, position_of_centre: Position, dimensions_to_crop: Dimensions):
        self._compose()
        x_center, y_center = position_of_centre.horizontal_vertical_tuple()
        width, height = dimensions_to_crop.width_height_tuple()
        self.clip = crop(
            self.clip, x_center=x_center, y_center=y_center, width=width, height=height
        )

    def normalize_audio(self):
        self.clip = self.clip.fx(afx.audio_normalize)

    def save(self, path: Path, codec="libx264", threads=1):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._compose()
        file_extension = str(path).split(".")[-1]
        if file_extension.lower() == "gif":
            self.clip.write_gif(
                str(path), fps=self.fps, fuzz=self.fuzz, verbose=False, logger=None
            )
        else:
            self.clip.write_videofile(
                str(path), fps=self.fps, codec=codec, verbose=False, logger=None, audio_codec="aac", threads=threads
            )

    def bytes(self) -> bytes:
        self._compose()
        with TemporaryDirectory(prefix="my_dear_tmp_") as directory:
            file_path = Path(directory) / "video.mp4"
            self.save(file_path)
            with open(file_path, "rb") as bytes_file:
                return bytes_file.read()

    def _compose(self):
        if self._children:
            entire_clip_duration = self.clip.duration
            # retarded bug in moviepy library has forced my hand to do this stupid shit
            # somehow after creating the composite video clip the duration is not set
            # as of 2021-11-08
            clips = [self.clip]
            for child in self._children:
                clips.append(child)
            self.clip = CompositeVideoClip(clips)
            self.clip.duration = entire_clip_duration
            self._children = []

    def apply_effect(self, effect: Effect):
        pass


def concatenate_video_clips(video_clips: List[VideoClip], method="chain"):
    return VideoClip(
        concatenate_videoclips(
            [video_clip.clip for video_clip in video_clips], method=method
        )
    )
