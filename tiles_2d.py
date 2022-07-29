import random
import math

import tiles


GRID_SIZE = 4


def render_2d_tile(tile):
    return {
        tile_conn(t12): '┘', tile_conn(t13): '─',
        tile_conn(t14): '┐', tile_conn(t23): '└',
        tile_conn(t24): '│', tile_conn(t34): '┌',
        tile_conn(t123): '┴', tile_conn(t124): '┤',
        tile_conn(t134): '┬', tile_conn(t234): '├',
        tile_conn(t1234): '┼',
    }.get(tile_conn(tile), '?')


def render_2d_state(cells):
    num_rows = math.floor(len(cells) / GRID_SIZE)
    rows = [cells[GRID_SIZE * i:GRID_SIZE * (i + 1)] for i in range(num_rows)]
    for row in rows:
        print(''.join(render_2d_tile(cell.tile) for cell in row))


if __name__ == '__main__':
    
    t12 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 0, tiles.Directions.DOWN: 0,
    }
    t13 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 0,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 0,
    }
    t14 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 0,
        tiles.Directions.RIGHT: 0, tiles.Directions.DOWN: 1,
    }
    t23 = {
        tiles.Directions.LEFT: 0, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 0,
    }
    t24 = {
        tiles.Directions.LEFT: 0, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 0, tiles.Directions.DOWN: 1,
    }
    t34 = {
        tiles.Directions.LEFT: 0, tiles.Directions.UP: 0,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 1,
    }
    t123 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 0,
    }
    t124 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 0, tiles.Directions.DOWN: 1,
    }
    t134 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 0,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 1,
    }
    t234 = {
        tiles.Directions.LEFT: 0, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 1,
    }
    t1234 = {
        tiles.Directions.LEFT: 1, tiles.Directions.UP: 1,
        tiles.Directions.RIGHT: 1, tiles.Directions.DOWN: 1,
    }
    
    def tile_conn(tile):
        if not tile:
            return ()
        return (
            tile[tiles.Directions.LEFT],
            tile[tiles.Directions.UP],
            tile[tiles.Directions.RIGHT],
            tile[tiles.Directions.DOWN],
        )
    
    tile_set = [t12, t13, t14, t23, t24, t34, t123, t124, t134, t234, t1234]
    for tile in tile_set:
        print(render_2d_tile(tile))
    
    
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
    
    

