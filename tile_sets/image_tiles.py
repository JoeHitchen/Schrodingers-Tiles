from typing import List, Tuple, Dict, TypedDict
import enum

import grids

from .tile_types import Tile, Connector


ConnectorsSpec = Tuple[Connector, Connector, Connector, Connector]
TilePrototypeMap = Dict[enum.Enum, 'TilePrototype']


class TilePrototype(TypedDict):
    connectors: ConnectorsSpec
    rotations: int



def _connectors_from_spec(
    connectors: ConnectorsSpec,
    rotation: int,
) -> Dict[grids.Direction, Connector]:
    
    directions = [
        grids.Direction.LEFT, grids.Direction.UP,
        grids.Direction.RIGHT, grids.Direction.DOWN,
    ]
    cycled_connectors = connectors[-rotation:] + connectors[:-rotation]
    
    return {
        direction: connector
        for direction, connector in zip(directions, cycled_connectors)
    }


def create_tiles_from_prototypes(prototypes: TilePrototypeMap) -> List[Tile]:
    
    tiles = []
    for tile_type, tile_prototype in prototypes.items():
        for rotation in range(tile_prototype['rotations']):
            tiles.append(Tile(
                tile_type.value,
                _connectors_from_spec(tile_prototype['connectors'], rotation),
            ))
    return tiles

