import random

import wave_functions


class CliRunner():
    
    def __init__(self, wave_function: wave_functions.WaveFunction):
        self.wave_function = wave_function
    
    def render_state(self) -> None:
        pass
    
    def inline_tile_string(self, tile: wave_functions.Tile) -> str:
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

