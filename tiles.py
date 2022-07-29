from dataclasses import dataclass
from typing import List
import random

GRID_SIZE = 9


@dataclass
class Tile:
    left: int
    right: int
    
    def __repr__(self):
        return f'Tile({self.left}-{self.right})'


@dataclass
class Cell:
    state: List[Tile]
    
    @property
    def collapsed(self):
        return len(self.state) == 1
    
    @property
    def tile(self):
        return self.state[0] if self.collapsed else None
    
    @tile.setter
    def tile(self, tile):
        self.state = [tile]


def collapse(wave_function, cell_index, tile):
    
    wave_function[cell_index].tile = tile
    
    inwards_conn = {wave_function[cell_index].tile.left}
    for cell in wave_function[max(cell_index-1, 0)::-1]:
        
        if cell == wave_function[cell_index]:  # Prevent accidental wrap-around
            break
        
        original_outwards_conn = {tile.left for tile in cell.state}
        cell.state = [tile for tile in cell.state if tile.right in inwards_conn]
        new_outwards_conn = {tile.left for tile in cell.state}
        if new_outwards_conn == original_outwards_conn:
            break
        inwards_conn = new_outwards_conn
    
    inwards_conn = {wave_function[cell_index].tile.right}
    for cell in wave_function[cell_index+1:]:
    
        original_outwards_conn = {tile.right for tile in cell.state}
        cell.state = [tile for tile in cell.state if tile.left in inwards_conn]
        new_outwards_conn = {tile.right for tile in cell.state}
        if new_outwards_conn == original_outwards_conn:
            break
        inwards_conn = new_outwards_conn


def get_most_contrained_cell(wave_function):
    
    possibility_space = {
        cell_index: len(cell.state)
        for cell_index, cell
        in enumerate(wave_function)
        if not cell.collapsed  # Ignore already collapsed cells
    }
    most_constrained_size = min(possibility_space.values())
    possibility_space = {
        cell_index: size
        for cell_index, size in possibility_space.items()
        if size == most_constrained_size
    }
    return random.choice(list(possibility_space.keys()))


def render_state(wave_function):
    
    def render_tile(tile, line):
        left = tile.left if tile else '?'
        right = tile.right if tile else '?'
        return {
            0: '╔══╗',
            1: f'║{left}{right}║',
            2: '╚══╝'
        }[line]
    
    # Selected tiles
    selected_tiles = [cell.tile for cell in wave_function]
    for line in range(3):
        tile_strings = [render_tile(tile, line) for tile in selected_tiles]
        print('  ' + ' '.join(tile_strings) + '  ')
    
    print((5 * len(wave_function) + 3) * '=')
    
    # Cell options
    for i in range(max(len(cell.state) for cell in wave_function)):
        for line in range(3):
            tile_strings = []
            for cell in wave_function:
                tile_strings.append(render_tile(cell.state[i], line) if i < len(cell.state) else '    ')
            print('  ' + ' '.join(tile_strings) + '  ')


if __name__ == '__main__':
    
    t11 = Tile(left = 1, right = 1)
    t12 = Tile(left = 1, right = 2)
    t22 = Tile(left = 2, right = 2)
    t23 = Tile(left = 2, right = 3)
    t33 = Tile(left = 3, right = 3)
    t34 = Tile(left = 3, right = 4)
    t44 = Tile(left = 4, right = 4)
    
    all_tiles = [t11, t12, t22, t23, t33, t34, t44]
    
    
    print('Initial State...')    
    wave_function = [Cell(state = all_tiles) for _ in range(GRID_SIZE)]
    render_state(wave_function)
    
    while any([not cell.collapsed for cell in wave_function]):
        print('')
        print('Performing random collapse...')
        cell_index = get_most_contrained_cell(wave_function)
        tile = random.choice(wave_function[cell_index].state)
        
        print('Selected {} at position {}'.format(tile, cell_index))
        collapse(wave_function, cell_index, tile)
        render_state(wave_function)

