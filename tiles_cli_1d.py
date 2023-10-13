from typing import Optional

from tile_sets import Tile, sequential_dominoes
import wave_functions
import grids
import cli


class CliRunner1D(cli.CliRunner):

    def __init__(self, wave_function: wave_functions.WaveFunction, polarised: bool):
        super().__init__(wave_function)
        self.polarised = polarised


    @staticmethod
    def inline_tile_string(tile: Optional[Tile]) -> str:
        return tile.id if tile else '?/?'

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
            print('  ' + '  '.join(tile_strings) + '  ')

        print((8 * len(self.wave_function.cells) + (15 if cyclic else 3)) * '=')

        # Cell options
        for i in range(max(len(cell.state) for cell in self.wave_function.cells)):
            for line in range(3):
                tile_strings = []
                for cell in self.wave_function.cells:
                    tile_strings.append((
                        self._render_tile(cell.state[i], line)
                        if i < len(cell.state) else '     '
                    ))
                padding = (9 if cyclic else 2) * ' '
                print(padding + '  '.join(tile_strings) + padding)


    def _render_tile(self, tile: Optional[Tile], line: int) -> str:

        if not self.polarised:
            return {
                0: '╔═══╗',
                1: '║{}║'.format(self.inline_tile_string(tile)),
                2: '╚═══╝',
            }[line]

        if tile:
            left = tile.connectors[grids.Direction.LEFT]
            right = tile.connectors[grids.Direction.RIGHT]
            mid_string = f'{left.style[:-1]}{right.style[:-1]}'
        else:
            mid_string = '??'

        return {
            0: '-════+',
            1: '- {} +'.format(mid_string),
            2: '-════+',
        }[line]


if __name__ == '__main__':

    # Options
    NUM_CONN = 6
    GRID_SIZE = 8
    GRID_CYCLIC = True
    POLARISED = False

    # Execution
    grid = grids.Grid1D(GRID_SIZE, GRID_CYCLIC)
    connectors, tile_set = sequential_dominoes(NUM_CONN, GRID_CYCLIC, POLARISED)
    wave_function = wave_functions.WaveFunction(grid, tile_set)

    if not GRID_CYCLIC:
        wave_function.apply_boundary_constraint(
            grids.Direction.RIGHT,  # Left boundary acts rightwards
            {connectors[0]},
        )
        wave_function.apply_boundary_constraint(
            grids.Direction.LEFT,  # Right boundary acts leftwards
            {connectors[-1]},
        )

    CliRunner1D(wave_function, POLARISED).run()

