import math

class vec2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, vec2_v):
        self.x = self.x + vec2_v.x
        self.y = self.y + vec2_v.y

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def get_direction(self):
        if self.y == 0:
            if self.x > 0:
                return 0
            elif self.x < 0:
                return math.pi
            else:
                return 10
        if self.x == 0:
            if self.y > 0:
                return math.pi / 2
            else:
                return -math.pi / 2
        return math.atan(self.y / (-self.x))

    def discretize(self):
        self.x = int(round(self.x))
        self.y = int(round(self.y))

    def __str__(self):
        return "(%.3g, %.3g)" % (self.x, self.y)
