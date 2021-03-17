from coordinates import Coordinate
import matplotlib.patches as patches


class Block:
    def __init__(self, _width, _height, _center):
        """
        Create a new block given width and height

        Parameters:
        -----------

        width : double
            Represent the width of the block in meters
        height : double
            Represent the height of the block in meters
        """
        self.width = _width
        self.height = _height
        self.center = _center

    def update_position(self, _x, _y):
        print(_x)
        print(_y)
        self.center = self.center + Coordinate(x=_x, y=_y)

    def draw(self):
        return patches.Rectangle(
                (
                    self.center.x - (self.width / 2),
                    self.center.y - (self.height / 2)
                ),
                self.width,
                self.height,
                fill='C0'
            )
