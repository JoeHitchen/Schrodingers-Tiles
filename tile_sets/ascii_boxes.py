"""Describes a set of ASCII box-art tiles that can be single or double ruled."""
from typing import List, Tuple

import grids

from . import Tile, Connector

ConnectorsSpec = List[Connector]


def _generate_tiles_from_spec(
    connectors: ConnectorsSpec,
    rotations: List[int],
    symbols: str,
) -> List[Tile]:

    def _rotate_connectors(connectors: ConnectorsSpec, num_places: int) -> ConnectorsSpec:
        return connectors[-num_places:] + connectors[:-num_places]

    tiles = []
    for rotation in rotations:
        rotated_connectors = _rotate_connectors(connectors, rotation)

        tiles.append(Tile(
            symbols[rotation],
            {
                grids.Direction.LEFT: rotated_connectors[0],
                grids.Direction.UP: rotated_connectors[1],
                grids.Direction.RIGHT: rotated_connectors[2],
                grids.Direction.DOWN: rotated_connectors[3],
            },
        ))

    return tiles


def create() -> Tuple[List[Connector], List[Tile]]:

    # Define connectors
    c0 = Connector('0')
    c1 = Connector('1')
    c2 = Connector('2')
    connectors = [c0, c1, c2]

    # Define tile specs
    tile_specs: List[Tuple[ConnectorsSpec, List[int], str]] = [
        ([c0, c0, c0, c0], [0], ' '),
        ([c1, c1, c0, c0], [0, 1, 2, 3], '┘└┌┐'),
        ([c1, c1, c1, c0], [0, 1, 2, 3], '┴├┬┤'),
        ([c1, c0, c1, c0], [0, 1], '─│'),
        ([c1, c1, c1, c1], [0], '┼'),
        ([c2, c2, c0, c0], [0, 1, 2, 3], '╝╚╔╗'),
        ([c2, c2, c2, c0], [0, 1, 2, 3], '╩╠╦╣'),
        ([c2, c0, c2, c0], [0, 1], '═║'),
        ([c2, c2, c2, c2], [0], '╬'),
        ([c1, c2, c0, c0], [0, 1, 2, 3], '╜╘╓╕'),
        ([c1, c2, c1, c0], [0, 1, 2, 3], '╨╞╥╡'),
        ([c1, c2, c1, c2], [0], '╫'),
        ([c2, c1, c0, c0], [0, 1, 2, 3], '╛╙╒╖'),
        ([c2, c1, c2, c0], [0, 1, 2, 3], '╧╟╤╢'),
        ([c2, c1, c2, c1], [0], '╪'),
    ]

    # Generate tiles
    tiles: List[Tile] = []
    for tile_spec in tile_specs:
        tiles.extend(_generate_tiles_from_spec(*tile_spec))
    return connectors, tiles

