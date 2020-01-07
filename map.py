from hex import Hex


class Map():
    """The class for an overall map made of hexes"""

    def __init__(self, length=10, width=10, setting=0):
        """Initialize values from which to generate terrain"""
        self.length = length
        self.width = width
        self.setting = setting
        self.hexes = []
        self.len = 0
        self.generate()

    def generate(self):
        """Main function to create map"""
        for row in range(self.length):
            if row % 2 == 0:
                width = self.width
            else:
                width = self.width - 1

            for col in range(width):
                new_hex = Hex(self.len, None)
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


if __name__ == '__main__':
    map = Map(5, 5)
    for hex in map.hexes:
        print(f"id: {hex},\
    MR: {hex.MR}, BR: {hex.BR}, BL: {hex.BL},\
 ML: {hex.ML}, TL: {hex.TL}, TR: {hex.TR}")
