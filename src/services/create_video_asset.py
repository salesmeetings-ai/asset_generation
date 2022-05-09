from pathlib import Path
from tempfile import TemporaryFile, TemporaryDirectory

from domain import AudioClip, VideoClip, Image


VIDEO_FORMATS = {"mp4", "mkv"}
AUDIO_FORMATS = {"mp3", "wav"}
IMAGE_FORMATS = {"jpg", "jpeg", "png"}


class InvalidAssetFormat(Exception):
    pass


def video_asset_from_file(
    asset_bytes: bytes, asset_format: str
) -> AudioClip or VideoClip or Image:
    with TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / f"temp.{asset_format}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(asset_bytes)

            if asset_format in VIDEO_FORMATS:
                return VideoClip.from_path(temp_file_path)
            elif asset_format in AUDIO_FORMATS:
                return AudioClip.from_path(temp_file_path)
            elif asset_format in IMAGE_FORMATS:
                return Image.from_path(temp_file_path)

    raise InvalidAssetFormat(
        f"Invalid format *{asset_format}* supplied. "
        f"Acceptable formats are: {str({*AUDIO_FORMATS, *IMAGE_FORMATS, *VIDEO_FORMATS})}"
    )
