import cv2
from utils import Utils


class Spring:
    def __init__(self, _P, _Q):
        """
        Define a spring between two blocks.
        """
        self.P = _P
        self.Q = _Q
        self.k = 20  # N/m
        self.l_0 = 1/100

    def draw(self, frame, offset, invert_y):
        if invert_y:
            inv = -1
        else:
            inv = 1
            
        return cv2.line(
            frame,
            (
                Utils.ConvertX(self.P.x + offset.x),
                Utils.ConvertY(inv * (self.P.y) + offset.y)
            ),
            (
                Utils.ConvertX(self.Q.x + offset.x),
                Utils.ConvertY(inv * (self.Q.y) + offset.y)
            ),
            (0, 100, 100),
            thickness=3
        )
