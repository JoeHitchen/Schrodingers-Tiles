from dataclasses import dataclass
from typing import List, Dict
import random
import enum

GRID_SIZE = 9


class Directions(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'


def dir_flip(direction):
    return Directions.LEFT if direction == Directions.RIGHT else Directions.RIGHT


Tile = Dict[Directions, int]


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
    
    @property
    def connectors(self):
        return {
            direction: {tile[direction] for tile in self.state}
            for direction in Directions
        }
    
    def constrain(self, direction, constraint):
        
        original_connectors = self.connectors
        self.state = [
            tile for tile in self.state
            if tile[dir_flip(direction)] in constraint
        ]
        
        return [
            {'direction': onward_direction, 'constraint': self.connectors[onward_direction]}
            for onward_direction in Directions
            if self.connectors[onward_direction] != original_connectors[onward_direction]
            and onward_direction != dir_flip(direction)
        ]


def collapse(wave_function, cell_index, tile):
    
    wave_function[cell_index].tile = tile
    
    propagation = [{
        'direction': Directions.LEFT,
        'constraint': wave_function[cell_index].connectors[Directions.LEFT],
    }]
    for cell in wave_function[max(cell_index - 1, 0)::-1]:
        if cell == wave_function[cell_index]:  # Prevent accidental wrap-around
            break
        
        propagation = cell.constrain(**propagation[0])
        if not propagation:
            break
    
    
    propagation = [{
        'direction': Directions.RIGHT,
        'constraint': wave_function[cell_index].connectors[Directions.RIGHT],
    }]
    for cell in wave_function[cell_index + 1:]:
        if cell == wave_function[cell_index]:  # Prevent accidental wrap-around
            break
        
        propagation = cell.constrain(**propagation[0])
        if not propagation:
            break


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
        left = tile[Directions.LEFT] if tile else '?'
        right = tile[Directions.RIGHT] if tile else '?'
        return {
            0: '╔══╗',
            1: f'║{left}{right}║',
            2: '╚══╝',
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
                tile_strings.append((
                    render_tile(cell.state[i], line)
                    if i < len(cell.state) else '    '
                ))
            print('  ' + ' '.join(tile_strings) + '  ')


if __name__ == '__main__':
    
    t11 = {Directions.LEFT: 1, Directions.RIGHT: 1}
    t12 = {Directions.LEFT: 1, Directions.RIGHT: 2}
    t22 = {Directions.LEFT: 2, Directions.RIGHT: 2}
    t23 = {Directions.LEFT: 2, Directions.RIGHT: 3}
    t33 = {Directions.LEFT: 3, Directions.RIGHT: 3}
    t34 = {Directions.LEFT: 3, Directions.RIGHT: 4}
    t44 = {Directions.LEFT: 4, Directions.RIGHT: 4}
    
    all_tiles = [t11, t12, t22, t23, t33, t34, t44]
    
    
    print('Initial State...')
    wave_function = [Cell(state = all_tiles) for _ in range(GRID_SIZE)]
    render_state(wave_function)
    
    while any([not cell.collapsed for cell in wave_function]):
        print('')
        print('Performing random collapse...')
        cell_index = get_most_contrained_cell(wave_function)
        tile = random.choice(wave_function[cell_index].state)
        
        print('Selected {}-{} at position {}'.format(
            tile[Directions.LEFT],
            tile[Directions.RIGHT],
            cell_index,
        ))
        collapse(wave_function, cell_index, tile)
        render_state(wave_function)

