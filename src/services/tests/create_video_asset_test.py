from services.create_video_asset import video_asset_from_file
import hashlib


def test_create_video_asset():
    with open("test_video.mp4", mode="rb") as file:
        video_bytes = file.read()

    asset = video_asset_from_file(video_bytes, "mp4")

    asset_bytes = asset.bytes()
    assert hashlib.md5(asset_bytes).hexdigest() == hashlib.md5(video_bytes).hexdigest()


