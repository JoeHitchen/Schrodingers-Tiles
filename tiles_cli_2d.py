from typing import List, Tuple, Optional

import wave_functions
import grids
import cli


def create_2d_ascii_box_tiles_and_symbols() -> List[Tuple[wave_functions.Tile, str]]:
    """Creates a set of ASCII box-art tiles that can be single or double ruled."""
    
    def _generate_tiles_and_symbols(
        spec: Tuple[int, int, int, int],
        symbols: List[str],
    ) -> List[Tuple[wave_functions.Tile, str]]:
        """Creates a set of tiles based on a set of symbols and a connection template."""
        
        tiles_and_symbols = [({
            grids.Direction.LEFT: spec[0],
            grids.Direction.UP: spec[1],
            grids.Direction.RIGHT: spec[2],
            grids.Direction.DOWN: spec[3],
        }, symbols[0])]
        
        for symbol in symbols[1:]:
            tiles_and_symbols.append(({
                grids.Direction.LEFT: tiles_and_symbols[-1][0][grids.Direction.DOWN],
                grids.Direction.UP: tiles_and_symbols[-1][0][grids.Direction.LEFT],
                grids.Direction.RIGHT: tiles_and_symbols[-1][0][grids.Direction.UP],
                grids.Direction.DOWN: tiles_and_symbols[-1][0][grids.Direction.RIGHT],
            }, symbol))
        
        return tiles_and_symbols
    
    
    return [
        *_generate_tiles_and_symbols((0, 0, 0, 0), [' ']),
        *_generate_tiles_and_symbols((1, 1, 0, 0), ['┘', '└', '┌', '┐']),
        *_generate_tiles_and_symbols((1, 1, 1, 0), ['┴', '├', '┬', '┤']),
        *_generate_tiles_and_symbols((1, 0, 1, 0), ['─', '│']),
        *_generate_tiles_and_symbols((1, 1, 1, 1), ['┼']),
        *_generate_tiles_and_symbols((2, 2, 0, 0), ['╝', '╚', '╔', '╗']),
        *_generate_tiles_and_symbols((2, 2, 2, 0), ['╩', '╠', '╦', '╣']),
        *_generate_tiles_and_symbols((2, 0, 2, 0), ['═', '║']),
        *_generate_tiles_and_symbols((2, 2, 2, 2), ['╬']),
        *_generate_tiles_and_symbols((1, 2, 0, 0), ['╜', '╘', '╓', '╕']),
        *_generate_tiles_and_symbols((1, 2, 1, 0), ['╨', '╞', '╥', '╡']),
        *_generate_tiles_and_symbols((1, 2, 1, 2), ['╫']),
        *_generate_tiles_and_symbols((2, 1, 0, 0), ['╛', '╙', '╒', '╖']),
        *_generate_tiles_and_symbols((2, 1, 2, 0), ['╧', '╟', '╤', '╢']),
        *_generate_tiles_and_symbols((2, 1, 2, 1), ['╪']),
    ]


class CliRunner2D(cli.CliRunner):
    
    def __init__(self, wave_function: wave_functions.WaveFunction) -> None:
        super().__init__(wave_function)
        
        self.tile_symbol_map = {
            self._tile_spec(tile): symbol
            for tile, symbol in create_2d_ascii_box_tiles_and_symbols()
        }
    
    
    def inline_tile_string(self, tile: Optional[wave_functions.Tile]) -> str:
        return self.tile_symbol_map.get(self._tile_spec(tile), '?')
    
    
    def render_state(self) -> None:
        
        grid = self.wave_function.grid
        rows = [
            self.wave_function.cells[grid.size_x * i:grid.size_x * (i + 1)]
            for i in range(grid.size_y)
        ]
        for row in rows:
            print(''.join(self.inline_tile_string(cell.tile) for cell in row))
    
    
    @staticmethod
    def _tile_spec(tile: Optional[wave_functions.Tile]) -> Optional[Tuple[int, int, int, int]]:
        if not tile:
            return None
        return (
            tile[grids.Direction.LEFT],
            tile[grids.Direction.UP],
            tile[grids.Direction.RIGHT],
            tile[grids.Direction.DOWN],
        )
        

if __name__ == '__main__':
    
    # Options
    GRID_SIZE = (16, 4)
    GRID_CYCLIC = (True, False)
    
    
    # Execution
    grid = grids.Grid2D(*GRID_SIZE, *GRID_CYCLIC)
    tile_set = [tile for tile, symbol in create_2d_ascii_box_tiles_and_symbols()]
    wave_function = wave_functions.WaveFunction(grid, tile_set)
    
    if not GRID_CYCLIC[1]:
        wave_function.apply_boundary_constraint(grids.Direction.DOWN, {0})  # Upper boundary
        wave_function.apply_boundary_constraint(grids.Direction.UP, {0})  # Lower boundary
    
    if not GRID_CYCLIC[0]:
        wave_function.apply_boundary_constraint(grids.Direction.RIGHT, {0})  # Left boundary
        wave_function.apply_boundary_constraint(grids.Direction.LEFT, {0})  # Right boundary
    
    CliRunner2D(wave_function).run()

