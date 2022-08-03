import enum

from .tile_types import Connector
from .image_tiles import TilePrototypeMap


conn_black = Connector('B')
conn_white = Connector('W')


class TileTypes(enum.Enum):
    BLACK_FULL = 'BF'
    BLACK_HALF = 'BH'
    BLACK_QUARTER = 'BQ'
    BLACK_TIMER = 'BT'
    WHITE_FULL = 'WF'
    WHITE_HALF = 'WH'
    WHITE_QUARTER = 'WQ'
    WHITE_TIMER = 'WT'
    

tile_prototypes: TilePrototypeMap = {
    TileTypes.BLACK_FULL: {
        'connectors': (conn_black, conn_black, conn_black, conn_black),
        'rotations': 1,
    },
    TileTypes.BLACK_HALF: {
        'connectors': (conn_white, conn_black, conn_white, conn_white),
        'rotations': 4,
    },
    TileTypes.BLACK_QUARTER: {
        'connectors': (conn_white, conn_black, conn_black, conn_white),
        'rotations': 4,
    },
    TileTypes.BLACK_TIMER: {
        'connectors': (conn_white, conn_black, conn_white, conn_black),
        'rotations': 2,
    },
    TileTypes.WHITE_FULL: {
        'connectors': (conn_white, conn_white, conn_white, conn_white),
        'rotations': 1,
    },
    TileTypes.WHITE_HALF: {
        'connectors': (conn_black, conn_white, conn_black, conn_black),
        'rotations': 4,
    },
    TileTypes.WHITE_QUARTER: {
        'connectors': (conn_black, conn_white, conn_white, conn_black),
        'rotations': 4,
    },
    TileTypes.WHITE_TIMER: {
        'connectors': (conn_black, conn_white, conn_black, conn_white),
        'rotations': 2,
    },
}

