# Schrödingers Tiles
A Python implementation of the Wave Function Collapse algorithm.

The wave function collapse algorithm is a procedural generation process that mimics the quantum mechanical namesake by initialising the output space into a superposition of all possible outcomes and then repeating a cycle of observation and propagation until the output has collapsed onto a single, self-consistent output state.
In the observation stage, a portion of the output most firmly constrained by previously information is selected and a single possible value selected.
This selection then provides a new set of constraints on its neighbours who have their own possibility space reduced, which can in turn generate new constraints on their neighbours as the information propagates outwards.
Once the wave function has reached a new, self-consistent state, the cycle of observation and propagation repeats.
The process continues until each portion of the output has been reduced to just a single possible value, at which point no further collapse is possible.


## Implementation
The project is based around the `Tile` object, which represent the building blocks for the pattern.
Each tile interfaces with its neighbours through a set of `Connector`s, with one presented for each direction in which the tile can be joined with another tile.
For a connection between two tiles to be valid, the connectors on either side must be compatible.
Currently, connectors can either match symmetrically with themselves, or antisymmetrically in a matched pair.
Tiles can be identified by an ID string, and `ImageTile`s also have a linked image for rendering the tile in the output.

Sets of images tiles are realisations of the `ImageTileSet` abstract base class.
When creating an instance of one of these tile sets, it is possible to create only a subset of the possible tiles by passing the constructor a list of values from that class's `TileTypes` subclass.
For example:
```
    GreenKnots([GreenKnots.TileTypes.CORNER, GreenKnots.TileTypes.LINE])
```
will create a set of green knots tiles which contain _only_ corner and straight pieces, whereas the default construction will create all possible tiles in the set, which here would also include blank, junction and crossover tiles.

The other key part of the implementation are the `WaveFunction` and `Cell` classes.
A wave function consists of a set of cells that are connected through a grid.
Each cell tracks its state - the set of tiles which it could be realised as - and its neighbour cells - defined by the grid used to construct the wave function.
Even when not fully collapsed, cells are able to infer the possible connections they could present and this information is used to propagate constraints through the wave function.
This propagation is performed on a cell-by-cell basis, but is managed by the overarching wave function through the `propagate_constraints` method.
When a new constraint is applied, the affected cell is updated and its state reduced as necessary.
The cell then inspects itself and determines if any of its interfaces now present a reduced set of connectors.
If this happens, then information about which neighbours are affected and the new constraint which affects them is passed back to the wave function.
The wave function then adds these to a propagation queue which is iterated through following the same process until every affected cell has been updated and none require further propagation.

However, one constraint and propagation is generally not sufficient to fully collapse the wave function and the "observation" stage of the algorithm can be performed one of two ways.
The `apply_boundary_constraint` wave function method allows the boundary to act on the wave function as a certain connector, and the `get_most_constrained_cell` can be used to select a cell to initiate a random collapse.

The whole process is currently triggered by scripts, with the script used depending on what tiles you wish to use.
The options are:
* `image_runner.py` generates images using both the Green Knots and Circles tile sets, with different configurations
* `tiles_cli_2d.py` generates a terminal output based on the unicode box tiles
* `tiles_cli_1d.py` generates a terminal output using a set of sequential dominoes


## Possible future directions
There are various directions that this coding challenge could be extended in future. A non-exhaustive list of ideas includes:

* Connector variants  
  _Connectors can currently only come in a self-matching symmetrical form, or a paired-but-antisymmetric couple.
  However, this is not sufficient for the adjacency rules of the [circuits tile set](https://github.com/mxgmn/WaveFunctionCollapse/tree/master/tilesets/Circuit) so a generalisation is required.
  This has also been opened for tracking (see [#1](https://github.com/JoeHitchen/Schrodingers-Tiles/issues/1)) and an implementation is underway._

* Weighted selection  
  _Currently each tile possibility is given an equal weighting, but this does not allow for deliberate biases towards certain types of tile to be introduced (except by stacking the deck with multiple copies).
  A method of defining non-uniform probabilities for tiles and propagating these probabilities when updating could lead to interesting behaviour and a better reflection of the physical process the algorithm derives it's name from._

* Non-complete grids  
  _It feels like there should be a connection with games such as [Carcassonne](https://en.wikipedia.org/wiki/Carcassonne) or the traditional [Dominoes](https://en.wikipedia.org/wiki/Dominoes), which involve placing tiles, but do not necessarily result in a "complete" grid of a set size at the end of the game.
  Rather than trying to create a program to play those games, the objective would simply be to place all the tiles and avoid holes in the board._

* Hexagonal tile patterns  
  _A modification of the grid data structures could allow for connections to be made along three hexagonal directions, rather than the two rectangular ones.
  The tiles used could be based around abstract [Serpentiles](https://en.wikipedia.org/wiki/Serpentiles) such as those used by [Tantrix](https://en.wikipedia.org/wiki/Tantrix), or world-building inspired designs like those of [Dorfromantik](https://www.gog.com/en/game/dorfromantik) or [Fjords](https://boardgamegeek.com/boardgame/15511/fjords)._

* More complicated two-dimensional grids  
  _Other regular patterns are also possible in two dimensions, with obvious examples being repeated triangles or a rectangular brick pattern.
  Of particular interest could be patterns of multiple shapes, such as octagons & squares, or (along with a dynamic grid) a kite & darts [Penrose tiling](https://en.wikipedia.org/wiki/Penrose_tiling)._

* Three-Dimensional cubic tile patterns  
  _While very similar in format to the existing square two-dimensional tile patterns, the challenge here will be finding an output engine which does justice to the structures which are created.
  A target could be the design of small islands, such as those found in [Bad North](https://www.badnorth.com/)._

* Pixel-by-pixel generation  
  _The original wave function collapse implementation also included a pixel-by-pixel method, whereby the state was managed on a pixel-by-pixel basis, and the constraints on those pixels were determined by considering patterns over a larger area (e.g. 3x3 selections) to allow irregular patterns to develop, such as in their flowers example._

* Sudoku  
  _A lot of discussions of Wave Function Collapse include a description of solving Sudoku puzzles, and this could be an interesting challenge to tackle, with the "random choice" collapse method being replaced by information from more complicated solution techniques._


## Further reading

Before starting this project, I came across a number of videos & articles on the wave function collapse algorithm which served as inspiration for this project, and which could be similarly useful to others.
In no particular order:

* [mxgmn/WaveFunctionCollapse](https://github.com/mxgmn/WaveFunctionCollapse) | Maxim Gumin  
  _Once again, the original introduction of wave function collapse, which also includes an extensive record of derived work._

* [The Wavefunction Collapse Algorithm explained very clearly](https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/) | Robert Heaton  
  _An article describing the algorithm and the propagation of adjacency constraints._

* [Superpositions, Sudoku, the Wave Function Collapse algorithm](https://www.youtube.com/watch?v=2SuvO4Gi7uY) | Martin Donald  
  _A discussion of how the algorithm works and how it can be implemented in three dimensions._

* [How Townscaper Works: A Story Four Games in the Making](https://www.youtube.com/watch?v=_1fvJ5sHh6A) | AI and Games  
  _An interview with [Oskar Stålberg](https://oskarstalberg.com/) about how wave function collapse is used in his games Bad North and [Townscraper](https://www.townscapergame.com/)._

* [Coding Challenge 171: Wave Function Collapse](https://www.youtube.com/watch?v=rI_y2GAlQFM) | The Coding Train  
  _A mostly-real-time implementation of the algorithm for T-shaped tiles and then the circuits tile set (but without the advanced constraints)._

