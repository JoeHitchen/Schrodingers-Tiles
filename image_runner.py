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
            if not cell.tile:
                continue
            output_image.paste(
                cast(ImageTile, cell.tile).image,
                (img_row * images_size[0], img_col * images_size[1]),
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

