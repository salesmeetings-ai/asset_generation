import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Tuple

from moviepy.editor import AudioFileClip
import numpy as np

log = logging.getLogger(__name__)


class AudioClip:
    def __init__(self, clip: AudioFileClip):
        self.clip = clip

    @property
    def duration(self):
        return self.clip.duration

    @classmethod
    def from_path(cls, path: Path):
        clip = AudioFileClip(str(path))
        return cls(clip=clip)

    @property
    def fps(self):
        return self.clip.fps

    def get_subclip(self, time_start: float, time_end: float):
        return AudioClip(self.clip.subclip(t_start=time_start, t_end=time_end))

    def strip_soundless_ends(self, activation_threshold=0.1, time_padding=0.1):
        timeline, audio_signal = self.get_time_and_mono_signal()
        audio_signal_normed = audio_signal / np.max(np.abs(audio_signal))
        time_where_signal_is_greater_than_threshold = timeline[
            np.abs(audio_signal_normed) > activation_threshold
        ]
        time_start = max(
            0,
            time_where_signal_is_greater_than_threshold[0] - time_padding,
        )
        time_end = min(
            self.duration,
            time_where_signal_is_greater_than_threshold[-1] + time_padding,
        )
        return self.get_subclip(time_start, time_end)

    def get_time_and_mono_signal(self) -> Tuple[np.ndarray, np.ndarray]:
        signal_array = self.to_soundarray()[:, :1].flatten()
        timeline = np.linspace(0, self.clip.duration, len(signal_array))
        return timeline, signal_array

    def to_soundarray(self):
        return self.clip.to_soundarray(fps=self.fps)

    def save(self, path: Path):
        self.clip.write_audiofile(
            str(path), fps=self.clip.fps, verbose=False, logger=None
        )

    def bytes(self):
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "audio.mp3"
            self.save(file_path)
            with open(file_path, "rb") as bytes_file:
                return bytes_file.read()
