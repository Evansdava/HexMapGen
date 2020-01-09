# Welcome to HexMapGen

This is a hex-based map generator for making small-scale battlemaps as would be used in Dungeons and Dragons, Lancer, or other tabletop RPGs.

## How it Works:

### Each hex on the map is an object of the Hex class. The hex object has several properties:

* An id number: keeping track of its position in the map
* References to the next adjacent hex on each side
* The contents of the hex (terrain)


### The map is itself an object of the Map class that contains all associated hex objects, as well as a few other properties:

* Length (the number of rows in the map)
* Width (The number of hexes in a particular row)
* Percentage chances for each type of terrain to appear in any given hex

### The different types of terrain have different chances to appear:

Rivers appear in lines that can wander or split, with a 2% chance to appear on any edge
Roads appear in straight lines, with a 3% chance to appear on any edge
Buildings can appear next to roads or other buildings, at a 15% chance
Forests can appear anywhere at a 10% chance, or 20% next to other forests
Anywhere without terrain is empty and has no modifier
