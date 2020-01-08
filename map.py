from hex import Hex
from random import random, choice


class Map():
    """The class for an overall map made of hexes"""

    def __init__(self, length=10, width=10):
        """Initialize values from which to generate terrain"""
        self.length = length
        self.width = width
        self.hexes = []
        self.len = 0
        self.generate()

    def __str__(self):
        """Return a string visualization of the map"""
        string = ""
        count = 0
        for hex in self.hexes:
            if hex.ML is None:
                if count % 2 == 0:
                    string += f"{hex}"
                else:
                    string += f" {hex}"
            if hex.MR is not None:
                string += f" {hex.MR}"
            else:
                string += '\n'
                count += 1
        return string

    def generate(self):
        """Main function to create map"""
        for row in range(self.length):
            if row % 2 == 0:
                width = self.width
            else:
                width = self.width - 1

            for col in range(width):
                new_hex = Hex(self.len, ".")
                self.hexes.append(new_hex)
                self.len += 1

                if row == 0:
                    if col == 0:
                        tup = (("", 0),)
                    else:
                        tup = (("ML", 2),)
                else:
                    if col == 0:
                        if row % 2 == 0:
                            tup = (("TR", self.width),)
                        else:
                            tup = (("TL", self.width + 1), ("TR", self.width))
                    elif col == width - 1 and row % 2 == 0:
                        tup = (("ML", 2), ("TL", self.width + 1))
                    else:
                        tup = (("ML", 2),
                               ("TL", self.width + 1),
                               ("TR", self.width))

                for side, num in tup:
                    try:
                        new_hex.connect(side, self.hexes[self.len - num])
                    except IndexError:
                        pass

    def generate_rivers(self):
        """First checks if a river starts in an edge hex, then extends any"""
        current_hex = self.hexes[0]
        river_starts = []
        while current_hex.MR is not None:
            if random() < 0.02:
                current_hex.terrain = "W"
                river_starts.append(current_hex)
            current_hex = current_hex.MR
        while current_hex.BL is not None:
            if random() < 0.02:
                current_hex.terrain = "W"
                river_starts.append(current_hex)
            if current_hex.BR is None:
                current_hex = current_hex.BL
            else:
                current_hex = current_hex.BR
        while current_hex.ML is not None:
            if random() < 0.02:
                current_hex.terrain = "W"
                river_starts.append(current_hex)
            current_hex = current_hex.ML
        while current_hex.TR is not None:
            if random() < 0.02:
                current_hex.terrain = "W"
                river_starts.append(current_hex)
            if current_hex.TL is None:
                current_hex = current_hex.TR
            else:
                current_hex = current_hex.TL

        for start in river_starts:
            current_hex = start
            if current_hex.ML is None:
                direction = "r"
            elif current_hex.MR is None:
                direction = "l"
            elif current_hex.BL is None:
                direction = "u"
            elif current_hex.TL is None:
                direction = "d"

            while current_hex is not None:
                print(self)
                current_hex.terrain = "W"
                current_hex = choice(current_hex.get_direction(direction))


if __name__ == '__main__':
    map = Map(29, 29)
    map.generate_rivers()
    print(map)
