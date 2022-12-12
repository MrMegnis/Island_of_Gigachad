class Vector:
    def __init__(self, *args, **kwargs):
        if "x1" in kwargs and "x2" in kwargs and "y1" in kwargs and "y2" in kwargs:
            self.x = kwargs["x2"] - kwargs["x1"]
            self.y = kwargs["y2"] - kwargs["y1"]
        elif "point1" in kwargs and "point2" in kwargs:
            self.x = kwargs["point2"][0] - kwargs["point2"][0]
            self.y = kwargs["point2"][1] - kwargs["point2"][2]
        else:
            self.x = args[2] - args[0]
            self.y = args[3] - args[1]
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y