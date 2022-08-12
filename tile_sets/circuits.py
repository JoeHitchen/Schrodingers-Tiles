from typing import List

from .tile_types import Connector, create_paired_connectors, create_stub_connector
from .image_tiles import ImageTileSet


conn_board = Connector('None')
conn_track = Connector('Track')
conn_cable = Connector('Cable')
conn_track_stub = create_stub_connector(conn_track)
conn_cable_stub = create_stub_connector(conn_cable)

conn_diag_a = Connector('Track-Diag-A', {conn_track, conn_track_stub})
conn_diag_b = Connector('Track-Diag-B', {conn_track, conn_track_stub})

conn_chip_body = Connector('Chip-Body')
conn_chip_body_stub = create_stub_connector(conn_chip_body)
conn_chip_edge_left, conn_chip_edge_right = create_paired_connectors('Chip-Edge')
conn_chip_corner_left = create_stub_connector(conn_chip_edge_right, 'Chip-Corner (+)')
conn_chip_corner_right = create_stub_connector(conn_chip_edge_left, 'Chip-Corner (-)')


class Circuits(ImageTileSet):
    
    images_size = (14, 14)
    boundary_connector = conn_board
    
    class TileTypes(ImageTileSet.TileTypes):
        BOARD = 'OO'
        TRACK_CORNER = 'TC'
        TRACK_STRAIGHT = 'TS'
        TRACK_JUNCTION = 'TJ'
        TRACK_START = 'BS'
        TRACK_CONNECT = 'BC'
        SINGLE_DIAG = 'SD'
        DOUBLE_DIAG = 'DD'
        CABLE_START = 'AS'
        CABLE_MIDDLE = 'AM'
        CABLE_BRIDGE = 'AB'
        CHIP_BODY = 'HB'
        CHIP_EDGE = 'HE'
        CHIP_CORNER = 'HC'
    
    best_tile_subset: List[ImageTileSet.TileTypes] = [  # Removes two tiles for better outputs
        TileTypes.BOARD,
        TileTypes.TRACK_STRAIGHT,
        TileTypes.TRACK_START,
        TileTypes.TRACK_CONNECT,
        TileTypes.SINGLE_DIAG,
        TileTypes.DOUBLE_DIAG,
        TileTypes.CABLE_START,
        TileTypes.CABLE_MIDDLE,
        TileTypes.CABLE_BRIDGE,
        TileTypes.CHIP_BODY,
        TileTypes.CHIP_EDGE,
        TileTypes.CHIP_CORNER,
    ]
    
    
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
            'connectors': (conn_board, conn_track_stub, conn_board, conn_board),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_track_start.png',
        },
        TileTypes.TRACK_CONNECT: {
            'connectors': (conn_track_stub, conn_board, conn_track_stub, conn_board),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_track_connect.png',
        },
        TileTypes.SINGLE_DIAG: {
            'connectors': (conn_board, conn_diag_a, conn_diag_b, conn_board),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_single_diagonal.png',
        },
        TileTypes.DOUBLE_DIAG: {
            'connectors': (conn_diag_b, conn_diag_a, conn_diag_b, conn_diag_a),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_double_diagonal.png',
        },
        TileTypes.CABLE_START: {
            'connectors': (conn_board, conn_cable_stub, conn_board, conn_track_stub),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_cable_start.png',
        },
        TileTypes.CABLE_MIDDLE: {
            'connectors': (conn_cable, conn_board, conn_cable, conn_board),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_cable_middle.png',
        },
        TileTypes.CABLE_BRIDGE: {
            'connectors': (conn_cable, conn_track_stub, conn_cable, conn_track_stub),
            'rotations': 2,
            'image_path': 'tile_sets/images/circuits_cable_bridge.png',
        },
        TileTypes.CHIP_BODY: {
            'connectors': (conn_chip_body, conn_chip_body, conn_chip_body, conn_chip_body),
            'rotations': 1,
            'image_path': 'tile_sets/images/circuits_chip_body.png',
        },
        TileTypes.CHIP_EDGE: {
            'connectors': (
                conn_chip_edge_left,
                conn_track_stub,
                conn_chip_edge_right,
                conn_chip_body_stub,
            ),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_chip_edge.png',
        },
        TileTypes.CHIP_CORNER: {
            'connectors': (conn_chip_corner_left, conn_board, conn_board, conn_chip_corner_right),
            'rotations': 4,
            'image_path': 'tile_sets/images/circuits_chip_corner.png',
        },
    }

