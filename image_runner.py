from typing import Tuple, cast
import random

from PIL import Image as pillow
from tile_sets import ImageTile, ImageTileSet, GreenKnots, Circles
import wave_functions
import grids


def generate_wave_function_image(
    wave_function: wave_functions.WaveFunction,
    images_size: Tuple[int, int],
) -> None:
    
    output_size = (
        wave_function.grid.size_x * images_size[0],
        wave_function.grid.size_y * images_size[1],
    )
    output_image = pillow.new('RGB', output_size)
    
    for i in range(0, wave_function.grid.size_x):
        for j in range(0, wave_function.grid.size_y):
            cell = wave_function.cells[i + j * wave_function.grid.size_x]
            if not cell.tile:
                continue
            output_image.paste(
                cast(ImageTile, cell.tile).image,
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

