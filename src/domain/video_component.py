from dataclasses import dataclass
from typing import List

from src.domain.command import Command


@dataclass
class VideoComponent:
    file: str
    commands: List[Command]
