from typing import List, Tuple, Optional, cast

from tile_sets import Tile, Connector
import wave_functions
import grids
import cli


def create_2d_ascii_box_tiles_and_symbols() -> List[Tuple[Tile, str]]:
    """Creates a set of ASCII box-art tiles that can be single or double ruled."""
    
    def _generate_tiles_and_symbols(
        spec: Tuple[Connector, Connector, Connector, Connector],
        symbols: List[str],
    ) -> List[Tuple[Tile, str]]:
        """Creates a set of tiles based on a set of symbols and a connection template."""
        
        tiles_and_symbols = [(Tile({
            grids.Direction.LEFT: spec[0],
            grids.Direction.UP: spec[1],
            grids.Direction.RIGHT: spec[2],
            grids.Direction.DOWN: spec[3],
        }), symbols[0])]
        
        for symbol in symbols[1:]:
            tiles_and_symbols.append((Tile({
                grids.Direction.LEFT: tiles_and_symbols[-1][0].connectors[grids.Direction.DOWN],
                grids.Direction.UP: tiles_and_symbols[-1][0].connectors[grids.Direction.LEFT],
                grids.Direction.RIGHT: tiles_and_symbols[-1][0].connectors[grids.Direction.UP],
                grids.Direction.DOWN: tiles_and_symbols[-1][0].connectors[grids.Direction.RIGHT],
            }), symbol))
        
        return tiles_and_symbols
    
    c0 = cast(Connector, 0)
    c1 = cast(Connector, 1)
    c2 = cast(Connector, 2)
    
    return [
        *_generate_tiles_and_symbols((c0, c0, c0, c0), [' ']),
        *_generate_tiles_and_symbols((c1, c1, c0, c0), ['┘', '└', '┌', '┐']),
        *_generate_tiles_and_symbols((c1, c1, c1, c0), ['┴', '├', '┬', '┤']),
        *_generate_tiles_and_symbols((c1, c0, c1, c0), ['─', '│']),
        *_generate_tiles_and_symbols((c1, c1, c1, c1), ['┼']),
        *_generate_tiles_and_symbols((c2, c2, c0, c0), ['╝', '╚', '╔', '╗']),
        *_generate_tiles_and_symbols((c2, c2, c2, c0), ['╩', '╠', '╦', '╣']),
        *_generate_tiles_and_symbols((c2, c0, c2, c0), ['═', '║']),
        *_generate_tiles_and_symbols((c2, c2, c2, c2), ['╬']),
        *_generate_tiles_and_symbols((c1, c2, c0, c0), ['╜', '╘', '╓', '╕']),
        *_generate_tiles_and_symbols((c1, c2, c1, c0), ['╨', '╞', '╥', '╡']),
        *_generate_tiles_and_symbols((c1, c2, c1, c2), ['╫']),
        *_generate_tiles_and_symbols((c2, c1, c0, c0), ['╛', '╙', '╒', '╖']),
        *_generate_tiles_and_symbols((c2, c1, c2, c0), ['╧', '╟', '╤', '╢']),
        *_generate_tiles_and_symbols((c2, c1, c2, c1), ['╪']),
    ]


class CliRunner2D(cli.CliRunner):
    
    def __init__(self, wave_function: wave_functions.WaveFunction) -> None:
        super().__init__(wave_function)
        
        self.tile_symbol_map = {
            self._tile_spec(tile): symbol
            for tile, symbol in create_2d_ascii_box_tiles_and_symbols()
        }
    
    
    def inline_tile_string(self, tile: Optional[Tile]) -> str:
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
    tile_set = [tile for tile, symbol in create_2d_ascii_box_tiles_and_symbols()]
    wave_function = wave_functions.WaveFunction(grid, tile_set)
    
    c0 = cast(Connector, 0)
    if not GRID_CYCLIC[1]:
        wave_function.apply_boundary_constraint(grids.Direction.DOWN, {c0})  # Upper boundary
        wave_function.apply_boundary_constraint(grids.Direction.UP, {c0})  # Lower boundary
    
    if not GRID_CYCLIC[0]:
        wave_function.apply_boundary_constraint(grids.Direction.RIGHT, {c0})  # Left boundary
        wave_function.apply_boundary_constraint(grids.Direction.LEFT, {c0})  # Right boundary
    
    CliRunner2D(wave_function).run()

