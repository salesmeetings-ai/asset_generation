import time
import webbrowser
from pathlib import Path

from domain.position import Position
from domain.video_clip import VideoClip


def timetest(input_func):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = input_func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Method Name - {input_func.__name__}, "
            f"Args - {args}, Kwargs - {kwargs}, "
            f"Execution Time - {end_time - start_time}"
        )

        return result

    return timed


@timetest
def create_video(threads=1):
    josiah_clip: VideoClip = VideoClip.from_path(
        path=Path("adding_masked_video_input_video.mp4")
    )
    add_cricle_mask_to_video(josiah_clip)

    save_circle_mask_video(josiah_clip, threads)

    background_clip = VideoClip.from_path(path=Path("genium_slide_LATAM.gif"))
    background_clip.change_speed(final_duration=josiah_clip.duration)
    position = Position(
        vertical=background_clip.get_dimensions().height
        - josiah_clip.get_dimensions().height,
        horizontal=0,
    )

    add_overlay_to_gif(background_clip, josiah_clip, position)

    save_entire_clip(background_clip, threads)


@timetest
def save_entire_clip(background_clip, threads):
    background_clip.save(Path("adding_masked_video_result.mp4"), threads=threads)


@timetest
def add_overlay_to_gif(background_clip, josiah_clip, position):
    background_clip.add_overlay(josiah_clip, position)


@timetest
def save_circle_mask_video(josiah_clip, threads):
    josiah_clip.save(Path("adding_masked_video_circle_crop.mp4"), threads=threads)


@timetest
def add_cricle_mask_to_video(josiah_clip):
    josiah_clip.add_circle_mask(radius=int(josiah_clip.get_dimensions().width / 2 - 7))


if __name__ == "__main__":

    create_video(threads=0)
