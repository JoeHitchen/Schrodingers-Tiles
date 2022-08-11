from typing import Tuple, Optional, cast
from functools import lru_cache
import random

from PIL import Image as pillow
from tile_sets import ImageTile, ImageTileSet, Circuits
import wave_functions
import grids


StateTuple = Tuple[ImageTile]


@lru_cache
def _render_state_vector(state: StateTuple, images_size: Tuple[int, int]) -> pillow.Image:
    avg = pillow.new('RGB', images_size)
    for count, tile in enumerate(state):
        avg = pillow.blend(avg, tile.image, 1. / (1. + count))
    return avg


def generate_wave_function_image(
    wave_function: wave_functions.WaveFunction,
    images_size: Tuple[int, int],
) -> None:
    
    output_grid_size = (
        wave_function.grid.size_x + 2 * wave_function.grid.cyclic_x,
        wave_function.grid.size_y + 2 * wave_function.grid.cyclic_y,
    )
    
    output_image_size = (
        output_grid_size[0] * images_size[0],
        output_grid_size[1] * images_size[1],
    )
    output_image = pillow.new('RGB', output_image_size)
    
    for img_row in range(0, output_grid_size[0]):
        for img_col in range(0, output_grid_size[1]):
            grid_row = (img_row - wave_function.grid.cyclic_x) % wave_function.grid.size_x
            grid_col = (img_col - wave_function.grid.cyclic_y) % wave_function.grid.size_y
            cell = wave_function.cells[grid_row + grid_col * wave_function.grid.size_x]
            output_image.paste(
                _render_state_vector(cast(StateTuple, tuple(cell.state)), images_size),
                (img_row * images_size[0], img_col * images_size[1]),
            )
    
    output_image.show()


def main(
    tile_set: ImageTileSet,
    grid_size: Tuple[int, int],
    cyclic: bool = False,
    display_every: Optional[int] = None,
) -> None:
    
    grid = grids.Grid2D(*grid_size, *(cyclic, cyclic))
    
    wave_function = wave_functions.WaveFunction(grid, tile_set.tiles)
    if not cyclic:
        for direction in grids.Direction:
            wave_function.apply_boundary_constraint(direction, {tile_set.boundary_connector})
    
    for i in range(grid.size_total):  # Iterations required ≤ Total number of grid cells
        if display_every and not i % display_every:
            generate_wave_function_image(wave_function, tile_set.images_size)
        
        cell = wave_function.get_most_constrained_cell()
        tile = random.choice(cell.state)
        print(f'Selected [{tile.id}] in {cell}')
        cell.tile = tile
        
        if wave_function.collapsed:
            break
    
    generate_wave_function_image(wave_function, tile_set.images_size)


if __name__ == '__main__':
    
    main(Circuits(Circuits.best_tile_subset), (64, 64), cyclic = False, display_every = 512)

