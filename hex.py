# from random import random


class Hex():
    """The class that governs individual hexes on the map"""

    def __init__(self, id_num, terrain):
        """Initializes the hex, setting the id number and relations"""
        self.id = id_num
        self.terrain = terrain
        self.BR = None
        self.MR = None
        self.BL = None
        self.ML = None
        self.TL = None
        self.TR = None

    def __str__(self):
        """Return a string representation of this hex"""
        return f"{self.terrain}"

    def connect(self, side, other):
        """Change the references of two hexes to match each other"""

        if side == "ML":
            self.ML = other
            other.MR = self
        elif side == "TL":
            self.TL = other
            other.BR = self
        elif side == "TR":
            self.TR = other
            other.BL = self
        elif side == "MR":
            self.MR = other
            other.ML = self
        elif side == "BR":
            self.BR = other
            other.TL = self
        elif side == "BL":
            self.BL = other
            other.TR = self

    def get_neighbors(self):
        """Return a tuple of all adjacent tiles"""
        return (self.MR, self.BR, self.BL, self.ML, self.TL, self.TR)

    def check_neighbors(self, keys=("."), exclude=False):
        """Return the neighbors of this hex that match, or don't, the key"""
        neighbors = []
        for tile in self.get_neighbors():
            if tile is None:
                if exclude:
                    neighbors.append(tile)
            else:
                if tile.terrain in keys and not exclude:
                    neighbors.append(tile)
                elif tile.terrain not in keys and exclude:
                    neighbors.append(tile)
        return neighbors

    def get_direction(self, dir):
        """Returns a tuple of neighbors in a certain direction (u/d/l/r)"""
        if dir == "u":
            return (self.ML, self.TL, self.TR, self.MR)
        if dir == "d":
            return (self.ML, self.BL, self.BR, self.MR)
        if dir == "r":
            return (self.TR, self.MR, self.BR)
        if dir == "l":
            return (self.BL, self.ML, self.TL)