from pathlib import Path

from domain import VideoClip


def create_video():
    josiah_clip: VideoClip = VideoClip.from_path(
        path=Path("adding_masked_video_input_video.mp4")
    )
    subclip = josiah_clip.get_subclip(0, 1)
    subclip.save(Path("test_video.mp4"))


if __name__ == "__main__":
    create_video()