import enum

from .tile_types import Connector
from .image_tiles import TilePrototypeMap


conn_none = Connector('None')
conn_pipe = Connector('Pipe')


class TileTypes(enum.Enum):
    EMPTY = 'O'
    CORNER = 'r'
    LINE = 'l'
    JUNCTION = 'T'
    CROSS = 'x'
    

tile_prototypes: TilePrototypeMap = {
    TileTypes.EMPTY: {
        'connectors': (conn_none, conn_none, conn_none, conn_none),
        'rotations': 1,
    },
    TileTypes.CORNER: {
        'connectors': (conn_none, conn_pipe, conn_pipe, conn_none),
        'rotations': 4,
    },
    TileTypes.LINE: {
        'connectors': (conn_pipe, conn_none, conn_pipe, conn_none),
        'rotations': 2,
    },
    TileTypes.JUNCTION: {
        'connectors': (conn_pipe, conn_none, conn_pipe, conn_pipe),
        'rotations': 4,
    },
    TileTypes.CROSS: {
        'connectors': (conn_pipe, conn_pipe, conn_pipe, conn_pipe),
        'rotations': 2,
    },
}

