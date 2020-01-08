from hex import Hex
from random import random, choice


class Map():
    """The class for an overall map made of hexes"""

    def __init__(self, length=15, width=15,
                 for_chance=0.1, riv_chance=0.02,
                 road_chance=0.02, build_chance=0.2):
        """Initialize values from which to generate terrain"""
        self.length = int(length)
        self.width = int(width)
        self.hexes = []
        self.len = 0
        self.for_chance = float(for_chance)
        self.riv_chance = float(riv_chance)
        self.road_chance = float(road_chance)
        self.build_chance = float(build_chance)
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

    def edge_crawl(self, key, chance):
        """Travels around edges and starts features"""
        current_hex = self.hexes[0]
        starts = []
        while current_hex.MR is not None:
            if random() < chance:
                current_hex.terrain = key
                starts.append(current_hex)
            current_hex = current_hex.MR
        while current_hex.BL is not None:
            if random() < chance:
                current_hex.terrain = key
                starts.append(current_hex)
            if current_hex.BR is None:
                current_hex = current_hex.BL
            else:
                current_hex = current_hex.BR
        while current_hex.ML is not None:
            if random() < chance:
                current_hex.terrain = key
                starts.append(current_hex)
            current_hex = current_hex.ML
        while current_hex.TR is not None:
            if random() < chance:
                current_hex.terrain = key
                starts.append(current_hex)
            if current_hex.TL is None:
                current_hex = current_hex.TR
            else:
                current_hex = current_hex.TL

        return starts

    def check_edge(self, tile):
        """Checks which edge a tile has and returns the opposite direction"""
        current_hex = tile
        if current_hex.ML is None:
            direction = "r"
        elif current_hex.MR is None:
            direction = "l"
        elif current_hex.BL is None:
            direction = "u"
        elif current_hex.TL is None:
            direction = "d"
        return direction

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

        self.generate_forests()
        self.generate_rivers()
        roads = self.generate_roads()
        self.generate_buildings(roads)

    def generate_forests(self):
        """Checks if random tiles or their neighbors are forests"""
        forests = []
        for _ in range(int(self.len / 10)):
            # print(self)
            current_hex = choice(self.hexes)
            if random() < self.for_chance:
                current_hex.terrain = "F"
                forests.append(current_hex)

        for tile in forests:
            for neighbor in tile.check_neighbors():
                # print(self)
                if random() < self.for_chance * 1.5:
                    neighbor.terrain = "F"
                    forests.append(neighbor)
        return forests

    def generate_rivers(self):
        """First checks if a river starts in an edge hex, then extends any"""
        river_starts = self.edge_crawl("W", self.riv_chance)
        rivers = river_starts.copy()

        for river in river_starts:
            direction = self.check_edge(river)
            current_hex = river

            while current_hex is not None:
                # print(self)
                current_hex.terrain = "W"
                rivers.append(current_hex)
                current_hex = choice(current_hex.get_direction(direction))[0]
        return rivers

    def generate_roads(self):
        """Chooses an edge tile and extends in a random direction"""
        road_starts = self.edge_crawl("R", self.road_chance)
        roads = road_starts.copy()

        for road in road_starts:
            direction = self.check_edge(road)
            if direction == "u":
                options = ("TL", "TR")
            elif direction == "d":
                options = ("BL", "BR")
            else:
                options = None
            straight = False
            path = choice(road.get_direction(direction))[1]
            current_hex = road

            if options is not None:
                if random() < 0.50:
                    path = choice(options)
                else:
                    path = options
                    straight = True

            if straight:
                while current_hex is not None:
                    for direction in path:
                        if current_hex is not None:
                            # print(self)
                            current_hex.terrain = "R"
                            roads.append(current_hex)
                            current_hex = current_hex.get_direction(direction)
            else:
                while current_hex is not None:
                    # print(self)
                    current_hex.terrain = "R"
                    roads.append(current_hex)
                    current_hex = current_hex.get_direction(path)
        return roads

    def generate_buildings(self, roads):
        """Makes buildings along each road and each building"""
        structures = roads.copy()
        buildings = []
        for structure in structures:
            tiles = structure.check_neighbors(("R", "W", "B"), True)
            for tile in tiles:
                if random() < self.build_chance:
                    # print(self)
                    tile.terrain = "B"
                    buildings.append(tile)
                    structures.append(tile)
        return buildings


if __name__ == '__main__':
    map = Map(29, 29)
    # map.generate_forests()
    # map.generate_rivers()
    # roads = map.generate_roads()
    # map.generate_buildings(roads)
    print(map)
