from .tile_types import Connector, create_paired_connectors
from .image_tiles import ImageTileSet


conn_board = Connector('None')
conn_track = Connector('Pipe')
conn_cable = Connector('Cable')
conn_chip_body = Connector('Chip-Body')
conn_chip_left, conn_chip_right = create_paired_connectors('Chip-Edge')


class Circuits(ImageTileSet):
    
    images_size = (14, 14)
    boundary_connector = conn_board
    
    class TileTypes(ImageTileSet.TileTypes):
        BOARD = 'O'
        TRACK_CORNER = 'TC'
        TRACK_STRAIGHT = 'TS'
        TRACK_JUNCTION = 'TJ'
        TRACK_START = 'TS'
        TRACK_CONNECT = 'TC'
        SINGLE_DIAG = 'SD'
        DOUBLE_DIAG = 'DD'
        CABLE_START = 'AS'
        CABLE_MIDDLE = 'AM'
        CABLE_BRIDGE = 'AB'
        CHIP_BODY = 'HB'
        CHIP_EDGE = 'HE'
        CHIP_CORNER = 'HC'
    
    
    tile_prototypes = {
        TileTypes.BOARD: {
            'connectors': (conn_board, conn_board, conn_board, conn_board),
            'rotations': 1,
            'image_path': 'tile_sets/images/circuits_board.png',
        },
        TileTypes.TRACK_CORNER: {
            'connectors': (conn_board, conn_track, conn_track, conn_board),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_track_corner.png',
        },
        TileTypes.TRACK_STRAIGHT: {
            'connectors': (conn_board, conn_track, conn_board, conn_track),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_track_straight.png',
        },
        TileTypes.TRACK_JUNCTION: {
            'connectors': (conn_track, conn_board, conn_track, conn_track),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_track_junction.png',
        },
        TileTypes.TRACK_START: {
            'connectors': (conn_board, conn_track, conn_board, conn_board),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_track_start.png',
        },
        TileTypes.TRACK_CONNECT: {
            'connectors': (conn_track, conn_board, conn_track, conn_board),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_track_connect.png',
        },
        TileTypes.SINGLE_DIAG: {
            'connectors': (conn_board, conn_track, conn_track, conn_board),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_single_diagonal.png',
        },
        TileTypes.DOUBLE_DIAG: {
            'connectors': (conn_track, conn_track, conn_track, conn_track),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_double_diagonal.png',
        },
        TileTypes.CABLE_START: {
            'connectors': (conn_board, conn_cable, conn_board, conn_track),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_cable_start.png',
        },
        TileTypes.CABLE_MIDDLE: {
            'connectors': (conn_cable, conn_board, conn_cable, conn_board),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_cable_middle.png',
        },
        TileTypes.CABLE_BRIDGE: {
            'connectors': (conn_cable, conn_track, conn_cable, conn_track),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_cable_bridge.png',
        },
        TileTypes.CHIP_BODY: {
            'connectors': (conn_chip_body, conn_chip_body, conn_chip_body, conn_chip_body),
            'rotations': 1,
            'image_path': 'tile_sets/images/circuits_chip_body.png',
        },
        TileTypes.CHIP_EDGE: {
            'connectors': (conn_chip_left, conn_track, conn_chip_right, conn_chip_body),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_chip_edge.png',
        },
        TileTypes.CHIP_CORNER: {
            'connectors': (conn_chip_left, conn_board, conn_board, conn_chip_right),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_chip_corner.png',
        },
    }

