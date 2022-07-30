from typing import List, Tuple, Optional
import random

import tiles


GRID_SIZE = (32, 8)
GRID_CYCLIC = (True, False)

light_corner = ['┘', '└', '┌', '┐']
light_tshape = ['┴', '├', '┬', '┤']
light_straight = ['─', '│']
light_cross = ['┼']

double_corner = ['╝', '╚', '╔', '╗']
double_tshape = ['╩', '╠', '╦', '╣']
double_straight = ['═', '║']
double_cross = ['╬']

light_double_corner = ['╜', '╘', '╓', '╕']
light_double_tshape = ['╨', '╞', '╥', '╡']
light_double_cross = ['╫']

double_light_corner = ['╛', '╙', '╒', '╖']
double_light_tshape = ['╧', '╟', '╤', '╢']
double_light_cross = ['╪']


def create_tiles_and_symbols(
    symbols: List[str],
    spec: Tuple[int, int, int, int],
) -> List[Tuple[tiles.Tile, str]]:
    """Creates a set of tiles based on a set of symbols and a connection template."""
    
    tiles_and_symbols = [({
        tiles.Directions.LEFT: spec[0],
        tiles.Directions.UP: spec[1],
        tiles.Directions.RIGHT: spec[2],
        tiles.Directions.DOWN: spec[3],
    }, symbols[0])]
    
    for symbol in symbols[1:]:
        tiles_and_symbols.append(({
            tiles.Directions.LEFT: tiles_and_symbols[-1][0][tiles.Directions.DOWN],
            tiles.Directions.UP: tiles_and_symbols[-1][0][tiles.Directions.LEFT],
            tiles.Directions.RIGHT: tiles_and_symbols[-1][0][tiles.Directions.UP],
            tiles.Directions.DOWN: tiles_and_symbols[-1][0][tiles.Directions.RIGHT],
        }, symbol))
    
    return tiles_and_symbols


def render_2d_state(cells: List[tiles.Cell]) -> None:
    rows = [cells[GRID_SIZE[0] * i:GRID_SIZE[0] * (i + 1)] for i in range(GRID_SIZE[1])]
    for row in rows:
        print(''.join(render_2d_tile(cell.tile) for cell in row))


if __name__ == '__main__':
    
    tiles_and_symbols = [
        *create_tiles_and_symbols([' '], (0, 0, 0, 0)),
        *create_tiles_and_symbols(light_corner, (1, 1, 0, 0)),
        *create_tiles_and_symbols(light_tshape, (1, 1, 1, 0)),
        *create_tiles_and_symbols(light_straight, (1, 0, 1, 0)),
        *create_tiles_and_symbols(light_cross, (1, 1, 1, 1)),
        *create_tiles_and_symbols(double_corner, (2, 2, 0, 0)),
        *create_tiles_and_symbols(double_tshape, (2, 2, 2, 0)),
        *create_tiles_and_symbols(double_straight, (2, 0, 2, 0)),
        *create_tiles_and_symbols(double_cross, (2, 2, 2, 2)),
        *create_tiles_and_symbols(light_double_corner, (1, 2, 0, 0)),
        *create_tiles_and_symbols(light_double_tshape, (1, 2, 1, 0)),
        *create_tiles_and_symbols(light_double_cross, (1, 2, 1, 2)),
        *create_tiles_and_symbols(double_light_corner, (2, 1, 0, 0)),
        *create_tiles_and_symbols(double_light_tshape, (2, 1, 2, 0)),
        *create_tiles_and_symbols(double_light_cross, (2, 1, 2, 1)),
    ]
    
    def tile_conn(tile: Optional[tiles.Tile]) -> Optional[Tuple[int, int, int, int]]:
        if not tile:
            return None
        return (
            tile[tiles.Directions.LEFT],
            tile[tiles.Directions.UP],
            tile[tiles.Directions.RIGHT],
            tile[tiles.Directions.DOWN],
        )
    
    def render_2d_tile(tile: Optional[tiles.Tile]) -> str:
        return {
            tile_conn(map_tile): map_symbol
            for map_tile, map_symbol in tiles_and_symbols
        }.get(tile_conn(tile), '?')
    
    tile_set = [tile for tile, symbol in tiles_and_symbols]
    
    
    wave_function = tiles.WaveFunction([
        tiles.Cell(id = f'{i + 1}-{j + 1}', state = tile_set)
        for j in range(GRID_SIZE[1]) for i in range(GRID_SIZE[0])
    ])
    tiles.link_2d_grid(wave_function.cells, GRID_SIZE, GRID_CYCLIC)
    
    boundary_conditions: List[tiles.Propagation] = []
    
    if not GRID_CYCLIC[1]:
        for i in range(GRID_SIZE[0]):
            boundary_conditions.append({
                'cell': wave_function.cells[i],
                'direction': tiles.Directions.DOWN,
                'constraint': {0},
            })
            boundary_conditions.append({
                'cell': wave_function.cells[- i - 1],
                'direction': tiles.Directions.UP,
                'constraint': {0},
            })
    
    if not GRID_CYCLIC[0]:
        for j in range(GRID_SIZE[1]):
            boundary_conditions.append({
                'cell': wave_function.cells[GRID_SIZE[0] * j],
                'direction': tiles.Directions.RIGHT,
                'constraint': {0},
            })
            boundary_conditions.append({
                'cell': wave_function.cells[GRID_SIZE[0] * (j + 1) - 1],
                'direction': tiles.Directions.LEFT,
                'constraint': {0},
            })
    wave_function.propagate_constraints(boundary_conditions)
    
    
    print('Initial state')
    render_2d_state(wave_function.cells)
    
    while not wave_function.collapsed:
        print('')
        print('Performing random collapse...')
        cell = wave_function.get_most_constrained_cell()
        tile = random.choice(cell.state)
        print('Selected {} for {}'.format(render_2d_tile(tile), cell))
        
        cell.tile = tile
        render_2d_state(wave_function.cells)
    
    

