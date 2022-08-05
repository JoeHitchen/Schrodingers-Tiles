from typing import Tuple
import random

from PIL import Image as pillow
from tile_sets import ImageTileSet, GreenKnots, Circles
import wave_functions
import grids


def convert_index_1d_to_2d(grid: grids.Grid2D, index: int) -> Tuple[int, int]:
    return (index % grid.size_x, index // grid.size_x)


def generate_wave_function_image(
    wave_function: wave_functions.WaveFunction,
    images_size: Tuple[int, int],
) -> None:
    
    output_size = (
        wave_function.grid.size_x * images_size[0],
        wave_function.grid.size_y * images_size[1],
    )
    output_image = pillow.new('RGB', output_size)
    
    for index, cell in enumerate(wave_function.cells):
        i, j = convert_index_1d_to_2d(wave_function.grid, index)
        output_image.paste(
            cell.tile.image,
            (i * images_size[0], j * images_size[1]),
        )
    output_image.show()


def main(tile_set: ImageTileSet, cyclic: bool = False) -> None:
    
    grid = grids.Grid2D(*(16, 9), *(cyclic, cyclic))
    
    wave_function = wave_functions.WaveFunction(grid, tile_set.tiles)
    if not cyclic:
        for direction in grids.Direction:
            wave_function.apply_boundary_constraint(direction, {tile_set.boundary_connector})
    
    while not wave_function.collapsed:
        cell = wave_function.get_most_constrained_cell()
        tile = random.choice(cell.state)
        print(f'Selected [{tile.id}] in {cell}')
        cell.tile = tile
    
    generate_wave_function_image(wave_function, tile_set.images_size)


if __name__ == '__main__':
    
    main(GreenKnots([GreenKnots.TileTypes.CORNER, GreenKnots.TileTypes.LINE]), cyclic = False)
    main(Circles(), cyclic = True)

