import random

import tiles


class CliRunner():
    
    def __init__(self, wave_function: tiles.WaveFunction):
        self.wave_function = wave_function
    
    def render_state(self) -> None:
        pass
    
    def inline_tile_string(self, tile: tiles.Tile) -> str:
        pass
    
    def run(self) -> None:
        
        print('Initial state')
        self.render_state()
        
        while not self.wave_function.collapsed:
            cell = self.wave_function.get_most_constrained_cell()
            tile = random.choice(cell.state)
            print(f'Selected {self.inline_tile_string(tile)} in {cell}')
            
            cell.tile = tile
            self.render_state()

