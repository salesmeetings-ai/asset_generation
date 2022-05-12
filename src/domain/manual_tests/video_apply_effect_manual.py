import os
import webbrowser
from pathlib import Path

from src.domain import VideoClip
from src.domain.video_effects.slice import Slice
from src.domain.video_effects.apply_effects import apply_effects

dir = Path(os.path.abspath(__file__)).parent

video_clip = VideoClip.from_path(dir / "adding_masked_video_circle_crop.mp4")
effect = Slice(0, 2)
video_clip_new = apply_effects(video_clip, [effect])
tmp_path = dir / "tmp.mp4"
video_clip_new.save(tmp_path)

with open(tmp_path) as file:
    webbrowser.open_new(file.name)
