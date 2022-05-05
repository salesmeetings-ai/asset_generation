import webbrowser

from asset_creators.media_content.dimensions import Dimensions
from asset_creators.media_content.image import Image
from asset_creators.media_content.manual_tests import TEST_DIR
from asset_creators.media_content.position import Position

russian_flag = Image.from_path(TEST_DIR / "russian_flag.png")
russian_flag.resize(Dimensions(width=1000, height=600))

putin = Image.from_path(
    TEST_DIR / "putin.png", position=Position(vertical=300, horizontal=-300)
)
putin.resize(Dimensions(width=1000, height=300))

trollface = Image.from_path(
    TEST_DIR / "trollface.png", position=Position(vertical=300, horizontal=600)
)
trollface.resize(Dimensions(width=300, height=300))

try:
    russian_flag.add_all([russian_flag, putin])
except ValueError:
    print("Caught recursion successfully")

russian_flag.add_all([trollface, putin])
russian_flag.save(TEST_DIR / "wide_putin_trollface.png")

with open(TEST_DIR / "wide_putin_trollface.png") as image:
    webbrowser.open_new(image.name)
