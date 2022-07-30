import random
import math

import tiles


GRID_SIZE = 16

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


def create_tiles_and_symbols(symbols, spec):
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


def render_2d_state(cells):
    num_rows = math.floor(len(cells) / GRID_SIZE)
    rows = [cells[GRID_SIZE * i:GRID_SIZE * (i + 1)] for i in range(num_rows)]
    for row in rows:
        print(''.join(render_2d_tile(cell.tile) for cell in row))


if __name__ == '__main__':
    
    tiles_and_symbols = [
        *create_tiles_and_symbols(' ', (0, 0, 0, 0)),
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
    
    def tile_conn(tile):
        if not tile:
            return ()
        return (
            tile[tiles.Directions.LEFT],
            tile[tiles.Directions.UP],
            tile[tiles.Directions.RIGHT],
            tile[tiles.Directions.DOWN],
        )
    
    def render_2d_tile(tile):
        return {
            tile_conn(map_tile): map_symbol
            for map_tile, map_symbol in tiles_and_symbols
        }.get(tile_conn(tile), '?')
    
    tile_set = [tile for tile, symbol in tiles_and_symbols]
    
    
    wave_function = [tiles.Cell(id = str(i + 1), state = tile_set) for i in range(GRID_SIZE ** 2)]
    tiles.link_rectangular_2d_grid(wave_function, GRID_SIZE)
    
    
    print('Initial state')
    render_2d_state(wave_function)
    
    while any([not cell.collapsed for cell in wave_function]):
        print('')
        print('Performing random collapse...')
        cell_index = tiles.get_most_contrained_cell(wave_function)
        tile = random.choice(wave_function[cell_index].state)
        print('Selected {} for {}'.format(render_2d_tile(tile), wave_function[cell_index]))
        
        tiles.collapse(wave_function, cell_index, tile)
        render_2d_state(wave_function)
    
    

