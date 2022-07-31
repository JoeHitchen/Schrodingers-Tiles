from dataclasses import dataclass, field
from typing import List, Dict, TypedDict, Set, Optional
import random

import grids
from tile_sets import Tile, Connector


class Propagation(TypedDict):
    cell: 'Cell'
    direction: grids.Direction
    constraint: Set[Connector]


@dataclass
class Cell:
    id: str
    state: List[Tile]
    neighbours: Dict[grids.Direction, 'Cell'] = field(default_factory = dict)
    
    def __str__(self) -> str:
        return f'Cell {self.id}'
    
    
    def link_neighbour(self, neighbour: 'Cell', direction: grids.Direction) -> None:
        neighbour_direction = grids.flip_direction(direction)
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
        """Forces a collapse of the current cell and triggers a propagation wave."""
        self.state = [tile]
        
        WaveFunction.propagate_constraints([{
            'cell': self.neighbours[direction],
            'direction': direction,
            'constraint': self.connectors[direction],
        } for direction in self.neighbours])
    
    
    @property
    def connectors(self) -> Dict[grids.Direction, Set[Connector]]:
        return {
            direction: {
                tile.connectors[direction]
                for tile in self.state
                if direction in tile.connectors
            }
            for direction in grids.Direction
        }
    
    
    def constrain(
        self,
        direction: grids.Direction,
        constraint: Set[Connector],
    ) -> List[Propagation]:
        """Applies a constraint to the cell states and determines any onward propagations."""
        
        # Apply new constraint
        original_connectors = self.connectors
        self.state = [
            tile for tile in self.state
            if tile.connectors[grids.flip_direction(direction)] in constraint
        ]
        if not self.state:
            raise self.ConstraintError(f'{self} has no remaining state options')
        
        # Identify new onward constraints
        return [
            {
                'cell': self.neighbours[onward_direction],
                'direction': onward_direction,
                'constraint': self.connectors[onward_direction],
            }
            for onward_direction in self.neighbours
            if self.connectors[onward_direction] != original_connectors[onward_direction]
            and onward_direction != grids.flip_direction(direction)
        ]
    
    
    class ConstraintError(Exception):
        """Used when a collapsed cell has no valid states remaining."""
        pass


class WaveFunction:
    
    def __init__(self, grid: grids.Grid, tile_set: List[Tile]):
        self.grid = grid
        self.cells = [Cell(
            id = grid.make_cell_id(index),
            state = tile_set,
        ) for index in range(grid.size_total)]
        
        for cell_slice, direction, cyclic in self.grid.get_neighbour_slices():
            neighbour_cells = self.cells[cell_slice]
            for index, cell in enumerate(neighbour_cells[:-1]):
                cell.link_neighbour(neighbour_cells[index + 1], direction)
            if cyclic:
                neighbour_cells[-1].link_neighbour(neighbour_cells[0], direction)
    
    
    @property
    def collapsed(self) -> bool:
        return all(cell.collapsed for cell in self.cells)
    
    def get_most_constrained_cell(self) -> Cell:
        """Randomly selects a cell with the smallest possibility space remaining."""
        
        possibility_space = {
            cell_index: len(cell.state)
            for cell_index, cell
            in enumerate(self.cells)
            if not cell.collapsed  # Ignore already collapsed cells
        }
        most_constrained_size = min(possibility_space.values())
        possibility_space = {
            cell_index: size
            for cell_index, size in possibility_space.items()
            if size == most_constrained_size
        }
        return self.cells[random.choice(list(possibility_space.keys()))]
    
    
    def apply_boundary_constraint(
        self,
        direction: grids.Direction,
        constraint: Set[Connector],
    ) -> None:
        """Applies the constraint given in the specified direction and propagates it as needed.
        
        N.B. The direction is the direction _the constraint acts in_, not the direction of the
        boundary relative to the grid.
        """
        
        cell_slice = self.grid.get_boundary_slice(grids.flip_direction(direction))
        
        self.propagate_constraints([{
            'cell': cell, 'direction': direction, 'constraint': constraint,
        } for cell in self.cells[cell_slice]])
    
    
    @staticmethod
    def propagate_constraints(propagations: List[Propagation]) -> None:
        """Iteratively applies constraints to cells until a consistent state is reached."""
        
        while propagations:
            propagation = propagations.pop(0)
            further_propagations = propagation['cell'].constrain(
                propagation['direction'],
                propagation['constraint'],
            )
            propagations.extend(further_propagations)

