class Position:
    def __init__(self, horizontal: int, vertical: int):
        self.horizontal = horizontal
        self.vertical = vertical

    def horizontal_vertical_tuple(self) -> tuple:
        return self.horizontal, self.vertical

    def copy(self):
        return Position(self.horizontal, self.vertical)
