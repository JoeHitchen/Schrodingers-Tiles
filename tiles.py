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

