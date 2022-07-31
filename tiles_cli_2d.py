from typing import Optional

from tile_sets import Tile, ascii_box_tiles
import wave_functions
import grids
import cli


class CliRunner2D(cli.CliRunner):
    
    @staticmethod
    def inline_tile_string(tile: Optional[Tile]) -> str:
        return tile.id if tile else '?'
    
    
    def render_state(self) -> None:
        
        grid = self.wave_function.grid
        rows = [
            self.wave_function.cells[grid.size_x * i:grid.size_x * (i + 1)]
            for i in range(grid.size_y)
        ]
        for row in rows:
            print(''.join(self.inline_tile_string(cell.tile) for cell in row))
        

if __name__ == '__main__':
    
    # Options
    GRID_SIZE = (16, 4)
    GRID_CYCLIC = (True, False)
    
    
    # Execution
    grid = grids.Grid2D(*GRID_SIZE, *GRID_CYCLIC)
    connectors, tile_set = ascii_box_tiles()
    wave_function = wave_functions.WaveFunction(grid, tile_set)
    
    if not GRID_CYCLIC[1]:
        wave_function.apply_boundary_constraint(
            grids.Direction.DOWN,  # Upper boundary acts downwards
            {connectors[0]},
        )
        wave_function.apply_boundary_constraint(
            grids.Direction.UP,  # Lower boundary acts upwards
            {connectors[0]},
        )
    
    if not GRID_CYCLIC[0]:
        wave_function.apply_boundary_constraint(
            grids.Direction.RIGHT,  # Left boundary acts rightwards
            {connectors[0]},
        )
        wave_function.apply_boundary_constraint(
            grids.Direction.LEFT,  # Right boundary acts leftwards
            {connectors[0]},
        )
    
    CliRunner2D(wave_function).run()

