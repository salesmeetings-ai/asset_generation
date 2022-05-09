from flask import Flask

app = Flask(__name__)


@app.route("/assemble_video")
def generate_vid():
    # concatenate
    # add circle mask
    #  mask
    # concatenate
    return "<p>Hello, World!</p>"


NATO_STANDARTS = {
    "output_format": "mp4",
    "files": {
        "video_1": {"hex": "abcdef", "format": "mp4"},
        "background_image": {"hex": "abcddd", "format": "jpeg"},
        "lip_sync_audio": {"hex": "abcddd", "format": "wav"},
    },
    "video_components": {
        0: [
            {
                "source_file": "background_image",
                "slice": {"start": 0, "end": 2},
                "position": [0, 0],
            },
        ],
        1: [
            {
                "source_file": "video_1",
                "position": [0, 0],
                "commands": [
                    {"slice": [0, 2]},
                    {"resize": [150, 150]},
                    {"circle_mask": ""},
                ],
            },
            {  # lip sync part
                "source_file": "video_1",
                "position": [0, 0],
                "commands": [
                    {"slice": [2, 3]},
                    {"lip_sync": "lip_sync_audio"},
                    {"resize": [150, 150]},
                    {"circle_mask": ""},
                ],
            },
            {
                "source_file": "video_1",
                "position": [0, 0],
                "commands": [
                    {"slice": [3, "end"]},
                    {"resize": [150, 150]},
                    {"circle_mask": ""},
                ],
            },
        ],
    },
}
