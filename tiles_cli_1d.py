from typing import Optional, cast

from tile_sets import Tile, Connector, sequential_dominoes
import wave_functions
import grids
import cli


class CliRunner1D(cli.CliRunner):
    
    @staticmethod
    def inline_tile_string(tile: Optional[Tile]) -> str:
        return tile.id if tile else '??'
    
    def render_state(self) -> None:
        
        cyclic = self.wave_function.grid.cyclic_x
        
        # Selected tiles
        selected_tiles = [cell.tile for cell in self.wave_function.cells]
        for line in range(3):
            tile_strings = [self._render_tile(tile, line) for tile in selected_tiles]
            if cyclic:
                tile_strings = [
                    '···' + tile_strings[-1][-2:],
                    *tile_strings,
                    tile_strings[0][:2] + '···',
                ]
            print('  ' + ' '.join(tile_strings) + '  ')
        
        print((5 * len(self.wave_function.cells) + (15 if cyclic else 3)) * '=')
        
        # Cell options
        for i in range(max(len(cell.state) for cell in self.wave_function.cells)):
            for line in range(3):
                tile_strings = []
                for cell in self.wave_function.cells:
                    tile_strings.append((
                        self._render_tile(cell.state[i], line)
                        if i < len(cell.state) else '    '
                    ))
                padding = (8 if cyclic else 2) * ' '
                print(padding + ' '.join(tile_strings) + padding)
    
    
    @classmethod
    def _render_tile(cls, tile: Optional[Tile], line: int) -> str:
        return {
            0: '╔══╗',
            1: '║{}║'.format(cls.inline_tile_string(tile)),
            2: '╚══╝',
        }[line]


if __name__ == '__main__':
    
    # Options
    NUM_CONN = 6
    GRID_SIZE = 10
    GRID_CYCLIC = False
    
    # Execution
    grid = grids.Grid1D(GRID_SIZE, GRID_CYCLIC)
    tile_set = sequential_dominoes(NUM_CONN, cyclic = GRID_CYCLIC)
    wave_function = wave_functions.WaveFunction(grid, tile_set)
    
    if not GRID_CYCLIC:
        c1 = cast(Connector, 1)
        cn = cast(Connector, NUM_CONN)
        wave_function.apply_boundary_constraint(grids.Direction.RIGHT, {c1})  # Left boundary
        wave_function.apply_boundary_constraint(grids.Direction.LEFT, {cn})  # Right boundary
    
    CliRunner1D(wave_function).run()

