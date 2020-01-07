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
        return f"{self.id}"

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
