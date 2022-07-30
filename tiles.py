from dataclasses import dataclass, field
from typing import List, Tuple, Dict, TypedDict, Set, Optional
import random
import enum

GRID_SIZE = 9
GRID_CYCLIC = True


class Directions(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'


def flip_direction(direction: Directions) -> Directions:
    return {
        Directions.LEFT: Directions.RIGHT,
        Directions.UP: Directions.DOWN,
        Directions.RIGHT: Directions.LEFT,
        Directions.DOWN: Directions.UP,
    }[direction]


def link_1d_grid(
    cells: List['Cell'],
    cyclic: bool = False,
    direction: Directions = Directions.RIGHT,
) -> None:
    """Connects cells in one direction, with an optional cyclical loop."""
    
    for index, cell in enumerate(cells[:-1]):
        cell.link_neighbour(cells[index + 1], direction)
    
    if cyclic:
        cells[-1].link_neighbour(cells[0], direction)


def link_2d_grid(
    cells: List['Cell'],
    grid_size: Tuple[int, int],
    grid_cyclic: Tuple[bool, bool],
) -> None:
    """Connects cells horizontally and vertically, with optional cyclical loops."""
    
    for j in range(grid_size[1]):
        link_1d_grid(cells[grid_size[0] * j:grid_size[0] * (j + 1)], grid_cyclic[0])
    
    for i in range(grid_size[0]):
        link_1d_grid(cells[i::grid_size[0]], grid_cyclic[1], Directions.DOWN)


Tile = Dict[Directions, int]


class Propagation(TypedDict):
    cell: 'Cell'
    direction: Directions
    constraint: Set[int]


class PropagationError(Exception):
    """Used when the wave-function collapse reaches an internally inconsistent state."""
    pass


@dataclass
class Cell:
    id: str
    state: List[Tile]
    neighbours: Dict[Directions, 'Cell'] = field(default_factory = dict)
    
    def __str__(self) -> str:
        return f'Cell {self.id}'
    
    
    def link_neighbour(self, neighbour: 'Cell', direction: Directions) -> None:
        neighbour_direction = flip_direction(direction)
        assert direction not in self.neighbours and neighbour_direction not in neighbour.neighbours
        
        self.neighbours[direction] = neighbour
        neighbour.neighbours[neighbour_direction] = self
        
    
    @property
    def collapsed(self) -> bool:
        return len(self.state) == 1
    
    @property
    def tile(self) -> Optional[Tile]:
        return self.state[0] if self.collapsed else None
    
    @tile.setter
    def tile(self, tile: Tile) -> None:
        self.state = [tile]
    
    @property
    def connectors(self) -> Dict[Directions, Set[int]]:
        return {
            direction: {tile[direction] for tile in self.state if direction in tile}
            for direction in Directions
        }
    
    def constrain(self, direction: Directions, constraint: Set[int]) -> List[Propagation]:
        
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


def collapse(wave_function: List[Cell], cell_index: int, tile: Tile) -> None:
    
    wave_function[cell_index].tile = tile
    
    propagations: List[Propagation] = [{
        'cell': wave_function[cell_index].neighbours[direction],
        'direction': direction,
        'constraint': wave_function[cell_index].connectors[direction],
    } for direction in wave_function[cell_index].neighbours]
    
    propagate_constraints(wave_function, propagations)


def propagate_constraints(wave_function: List[Cell], propagations: List[Propagation]) -> None:
    """Iteratively applies constraints to cells until a consistent state is reached."""
    
    while propagations:
        propagation = propagations.pop(0)
        cell = propagation['cell']
        further_propagations = cell.constrain(propagation['direction'], propagation['constraint'])
        propagations.extend(further_propagations)


def get_most_contrained_cell(wave_function: List[Cell]) -> int:
    
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

