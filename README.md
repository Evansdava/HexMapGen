Welcome to HexMapGen

##How it Works:

Each hex on the map is an object of the hex class. The hex object has several properties:

* An id number: keeping track of its position in the map
* References to the next adjacent hex on each side
* The contents of the hex (terrain)


The map is itself a class that contains all the hex objects, as well as a few other properties:

* Length (the number of rows in the map)
* Width (The number of hexes in a particular row)
* Percentage chances for each type of terrain to appear in any given hex