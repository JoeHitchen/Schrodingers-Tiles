from typing import List, Tuple, Dict, TypedDict
from dataclasses import dataclass
from functools import cached_property
import enum

from PIL import Image as pillow
import grids

from .tile_types import Tile, Connector


ConnectorsSpec = Tuple[Connector, Connector, Connector, Connector]
TilePrototypeMap = Dict[enum.Enum, 'TilePrototype']


class TilePrototype(TypedDict):
    connectors: ConnectorsSpec
    rotations: int
    image_path: str


class ImageSpec(TypedDict):
    path: str
    rotation: int


@dataclass
class ImageTile(Tile):
    image_spec: ImageSpec
    
    @cached_property
    def image(self) -> pillow.Image:
        img = pillow.open(self.image_spec['path'])
        return img.rotate(-90 * self.image_spec['rotation'])  # +ve rotation is anticlockwise


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


def create_tiles_from_prototypes(prototypes: TilePrototypeMap) -> List[ImageTile]:
    
    tiles = []
    for tile_type, tile_prototype in prototypes.items():
        for rotation in range(tile_prototype['rotations']):
            tiles.append(ImageTile(
                tile_type.value,
                _connectors_from_spec(tile_prototype['connectors'], rotation),
                {'path': tile_prototype['image_path'], 'rotation': rotation},
            ))
    return tiles

