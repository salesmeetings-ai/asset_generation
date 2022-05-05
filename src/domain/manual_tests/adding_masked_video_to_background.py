import time
import webbrowser
from pathlib import Path

from domain.position import Position
from domain.video_clip import VideoClip


def get_execution_time(func, args, kwargs):
    beginning = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    print(f"Execution time: {end-beginning}")


def create_video(threads=1):
    josiah_clip: VideoClip = VideoClip.from_path(
        path=Path("adding_masked_video_input_video.mp4")
    )
    josiah_clip.add_circle_mask(radius=int(josiah_clip.get_dimensions().width / 2 - 7))

    josiah_clip.save(Path("adding_masked_video_circle_crop.mp4"), threads=threads)
    background_clip = VideoClip.from_path(path=Path("genium_slide_LATAM.gif"))
    background_clip.change_speed(final_duration=josiah_clip.duration)
    position = Position(
        vertical=background_clip.get_dimensions().height
        - josiah_clip.get_dimensions().height,
        horizontal=0,
    )
    background_clip.add_overlay(josiah_clip, position)
    background_clip.save(Path("adding_masked_video_result.mp4"), threads=threads)

    with open(Path("adding_masked_video_result.mp4")) as image:
        webbrowser.open_new(image.name)


def get_performance_test_results():
    # get_execution_time(create_video, [1], {})
    get_execution_time(create_video, [0], {})


if __name__ == "__main__":

    get_performance_test_results()
