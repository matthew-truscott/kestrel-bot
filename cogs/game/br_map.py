import numpy as np

class BattleMap(object):
    def __init__(self, w, h):
        self.w = w;
        self.h = h;
        self.grid = np.zeros((h, w), dtype=float)
