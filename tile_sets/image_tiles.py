from abc import ABC
from typing import List, Tuple, Dict, TypedDict
from dataclasses import dataclass
from functools import cached_property
import enum

from PIL import Image as pillow
import grids

from .tile_types import Tile, Connector


ConnectorsSpec = Tuple[Connector, Connector, Connector, Connector]


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
    
    def __hash__(self) -> int:
        return hash(self.id)
    
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


class ImageTileSet(ABC):
    
    images_size: Tuple[int, int]
    boundary_connector: Connector
    tile_prototypes: Dict['TileTypes', 'TilePrototype']
    
    class TileTypes(enum.Enum):
        pass
    
    
    def __init__(self, tile_types: List[TileTypes] = []) -> None:
        """Generates the tiles for the tileset based on the subset provided."""
        
        filtered_tile_types = {
            tile_type: tile_prototype
            for tile_type, tile_prototype in self.tile_prototypes.items()
            if tile_type in (tile_types if tile_types else list(self.TileTypes))
        }
        
        self.tiles = []
        for tile_type, tile_prototype in filtered_tile_types.items():
            for rotation in range(tile_prototype['rotations']):
                self.tiles.append(ImageTile(
                    f'{tile_type.value}{rotation + 1}',
                    _connectors_from_spec(tile_prototype['connectors'], rotation),
                    {'path': tile_prototype['image_path'], 'rotation': rotation},
                ))

