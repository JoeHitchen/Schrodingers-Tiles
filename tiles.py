from dataclasses import dataclass, field
from typing import List, Dict
import random
import enum

GRID_SIZE = 9
GRID_CYCLIC = True


class Directions(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'


def flip_direction(direction):
    return Directions.LEFT if direction == Directions.RIGHT else Directions.RIGHT


def link_bounded_grid(cells):
    for index, cell in enumerate(cells[:-1]):
        cell.link_neighbour(cells[index + 1], Directions.RIGHT)


def link_cyclical_grid(cells):
    link_bounded_grid(cells)
    cells[-1].link_neighbour(cells[0], Directions.RIGHT)



Tile = Dict[Directions, int]


class PropagationError(Exception):
    """Used when the wave-function collapse reaches an internally inconsistent state."""
    pass


@dataclass
class Cell:
    state: List[Tile]
    neighbours: Dict[Directions, 'Cell'] = field(default_factory = dict)
    
    def link_neighbour(self, neighbour, direction):
        neighbour_direction = flip_direction(direction)
        assert direction not in self.neighbours and neighbour_direction not in neighbour.neighbours
        
        self.neighbours[direction] = neighbour
        neighbour.neighbours[neighbour_direction] = self
        
    
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
            if tile[flip_direction(direction)] in constraint
        ]
        if not self.state:
            raise PropagationError(f'{self} has no remaining state options')
        
        return [
            {
                'cell': self.neighbours[onward_direction],
                'direction': onward_direction,
                'constraint': self.connectors[onward_direction],
            }
            for onward_direction in self.neighbours
            if self.connectors[onward_direction] != original_connectors[onward_direction]
            and onward_direction != flip_direction(direction)
        ]


def collapse(wave_function, cell_index, tile):
    
    wave_function[cell_index].tile = tile
    
    propagations = [{
        'cell': wave_function[cell_index].neighbours[direction],
        'direction': direction,
        'constraint': wave_function[cell_index].connectors[direction],
    } for direction in wave_function[cell_index].neighbours]
    
    while propagations:
        propagation = propagations.pop(0)
        cell = propagation.pop('cell')
        further_propgations = cell.constrain(**propagation)
        propagations.extend(further_propgations)


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
    t41 = {Directions.LEFT: 4, Directions.RIGHT: 1}
    
    all_tiles = [t11, t12, t22, t23, t33, t34, t44, t41]
    
    
    wave_function = [Cell(state = all_tiles) for _ in range(GRID_SIZE)]
    grid_link_map = {True: link_cyclical_grid, False: link_bounded_grid}
    grid_link_map[GRID_CYCLIC](wave_function)
    
    print('Initial State...')
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

