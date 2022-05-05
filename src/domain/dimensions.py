class Dimensions:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @classmethod
    def from_width_height_tuple(cls, tuple_):
        width = tuple_[0]
        height = tuple_[1]
        return cls(width=width, height=height)

    def width_height_tuple(self) -> tuple:
        return self.width, self.height

    def copy(self):
        return Dimensions(self.width, self.height)
