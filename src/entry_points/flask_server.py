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
                "file": "background_image",
                "commands": [
                    {"slice": [0, "end"]},
                    {"set_position": [0, 0]},
                ],
            },
        ],
        1: [
            {
                "file": "video_1",
                "commands": [
                    {"slice": [0, 2]},
                    {"set_position": [0, 0]},
                    {"resize": [150, 150]},
                    {"circle_mask": ""},
                ],
            },
            {  # lip sync part
                "file": "video_1",
                "commands": [
                    {"slice": [2, 3]},
                    {"set_position": [0, 0]},
                    {"lip_sync": "lip_sync_audio"},
                    {"resize": [150, 150]},
                    {"circle_mask": ""},
                ],
            },
            {
                "file": "video_1",
                "commands": [
                    {"slice": [3, "end"]},
                    {"set_position": [0, 0]},
                    {"resize": [150, 150]},
                    {"circle_mask": ""},
                ],
            },
        ],
    },
}
