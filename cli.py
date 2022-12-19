from typing import Optional
import random

from tile_sets import Tile
import wave_functions


class CliRunner():
    
    def __init__(self, wave_function: wave_functions.WaveFunction):
        self.wave_function = wave_function
    
    def render_state(self) -> None:
        pass
    
    @staticmethod
    def inline_tile_string(tile: Optional[Tile]) -> str:
        return ''
    
    def run(self) -> None:
        
        print('Initial state')
        self.render_state()
        
        while not self.wave_function.collapsed:
            cell = self.wave_function.get_most_constrained_cell()
            tile = random.choice(cell.state)
            print(f'Selected [{self.inline_tile_string(tile)}] in {cell}')
            
            cell.tile = tile
            self.render_state()

