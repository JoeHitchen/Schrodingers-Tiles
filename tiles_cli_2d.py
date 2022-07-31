from typing import Tuple, Optional, cast

from tile_sets import Tile, Connector, ascii_box_tiles
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
    
    
    @staticmethod
    def _tile_spec(tile: Optional[Tile]) -> Optional[Tuple[int, int, int, int]]:
        if not tile:
            return None
        return (
            tile.connectors[grids.Direction.LEFT],
            tile.connectors[grids.Direction.UP],
            tile.connectors[grids.Direction.RIGHT],
            tile.connectors[grids.Direction.DOWN],
        )
        

if __name__ == '__main__':
    
    # Options
    GRID_SIZE = (16, 4)
    GRID_CYCLIC = (True, False)
    
    
    # Execution
    grid = grids.Grid2D(*GRID_SIZE, *GRID_CYCLIC)
    tile_set = ascii_box_tiles()
    wave_function = wave_functions.WaveFunction(grid, tile_set)
    
    c0 = cast(Connector, 0)
    if not GRID_CYCLIC[1]:
        wave_function.apply_boundary_constraint(grids.Direction.DOWN, {c0})  # Upper boundary
        wave_function.apply_boundary_constraint(grids.Direction.UP, {c0})  # Lower boundary
    
    if not GRID_CYCLIC[0]:
        wave_function.apply_boundary_constraint(grids.Direction.RIGHT, {c0})  # Left boundary
        wave_function.apply_boundary_constraint(grids.Direction.LEFT, {c0})  # Right boundary
    
    CliRunner2D(wave_function).run()

