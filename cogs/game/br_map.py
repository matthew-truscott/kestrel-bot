import numpy as np

class BattleMap(object):
    def __init__(self, w, h):
        self.w = w;
        self.h = h;
        self.grid = np.ones((h, w), dtype=int) * -1
        # generate setting - 0 = wilderness
        self.terrain = np.ones((h, w), dtype=int)
