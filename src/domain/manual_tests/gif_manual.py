import webbrowser

from asset_creators.media_content.dimensions import Dimensions
from asset_creators.media_content.image import Image
from asset_creators.media_content.manual_tests import TEST_DIR
from asset_creators.media_content.position import Position
from asset_creators.media_content.video_clip import VideoClip

video_clip = VideoClip.from_path(path=TEST_DIR / "genium_slide_LATAM.gif")

trollface = Image.from_path(
    TEST_DIR / "trollface.png", position=Position(vertical=300, horizontal=600)
)
trollface.resize(Dimensions(width=300, height=300))

video_clip.add_image(
    image=trollface, time_start=0.5, duration=video_clip.clip.duration - 0.5
)
video_clip.save(TEST_DIR / "genium_x_trollface.gif")

with open(TEST_DIR / "genium_x_trollface.gif") as image:
    webbrowser.open_new(image.name)
