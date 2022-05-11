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
        "image_logo": {"hex": "abcdef", "format": "jpeg"},
        "background_image": {"hex": "abcddd", "format": "jpeg"},
        "lip_sync_audio": {"hex": "abcddd", "format": "wav"},
    },
    "layers": {
        {
            "depth": 0,
            "commands": [],
            "video_components": [
                {
                    "file": "background_image",
                    "commands": [
                        {"set_duration": "something"},
                        {"set_position": [0, 0]},
                    ],
                },
            ],
        },
        {
            "depth": 1,
            "commands": [
                {"set_position": [0, 0]},
                {"resize": [150, 150]},
                {"circle_mask": ""},
            ],
            "video_components": [
                {
                    "file": "video_1",
                    "commands": [{"slice": [0, 2]}],
                },
                {  # lip sync part
                    "file": "video_1",
                    "commands": [
                        {"slice": [2, 3]},
                        {"lip_sync": "lip_sync_audio"},
                    ],
                },
                {
                    "file": "video_1",
                    "commands": [
                        {"add_image": "image_logo"},
                        {"slice": [3, "end"]},
                    ],
                },
            ],
        },
    },
}
