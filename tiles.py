from dataclasses import dataclass, field
from typing import List, Dict
import random
import enum

GRID_SIZE = 9
GRID_CYCLIC = True


class Directions(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'


def flip_direction(direction):
    return {
        Directions.LEFT: Directions.RIGHT,
        Directions.UP: Directions.DOWN,
        Directions.RIGHT: Directions.LEFT,
        Directions.DOWN: Directions.UP,
    }[direction]


def link_1d_grid(cells, cyclic = False, direction = Directions.RIGHT):
    """Connects cells in one direction, with an optional cyclical loop."""
    
    for index, cell in enumerate(cells[:-1]):
        cell.link_neighbour(cells[index + 1], direction)
    
    if cyclic:
        cells[-1].link_neighbour(cells[0], direction)


def link_2d_grid(cells, grid_size, grid_cyclic):
    """Connects cells horizontally and vertically, with optional cyclical loops."""
    
    for j in range(grid_size[1]):
        link_1d_grid(cells[grid_size[0] * j:grid_size[0] * (j + 1)], grid_cyclic[0])
    
    for i in range(grid_size[0]):
        link_1d_grid(cells[i::grid_size[0]], grid_cyclic[1], Directions.DOWN)


Tile = Dict[Directions, int]


class PropagationError(Exception):
    """Used when the wave-function collapse reaches an internally inconsistent state."""
    pass


@dataclass
class Cell:
    id: str
    state: List[Tile]
    neighbours: Dict[Directions, 'Cell'] = field(default_factory = dict)
    
    def __str__(self):
        return f'Cell {self.id}'
    
    
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
            direction: {tile[direction] for tile in self.state if direction in tile}
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
    
    propagate_constraints(wave_function, propagations)


def propagate_constraints(wave_function, constraints):
    """Iteratively applies constraints to cells until a consistent state is reached."""
    
    while constraints:
        constraint = constraints.pop(0)
        cell = constraint.pop('cell')
        further_constraints = cell.constrain(**constraint)
        constraints.extend(further_constraints)


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

