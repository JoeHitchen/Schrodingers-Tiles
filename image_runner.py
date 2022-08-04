from typing import List, Tuple
import random

from PIL import Image as pillow
from tile_sets.image_tiles import ImageTile, TilePrototypeMap, create_tiles_from_prototypes
from tile_sets import green_knots, circles
import grids


def convert_index_1d_to_2d(grid: grids.Grid2D, index: int) -> Tuple[int, int]:
    return (index % grid.size_x, index // grid.size_x)


def generate_wave_function_image(
    grid: grids.Grid2D,
    tiles: List[ImageTile],
    images_size: Tuple[int, int],
) -> None:
    
    output_size = (grid.size_x * images_size[0], grid.size_y * images_size[1])
    output_image = pillow.new('RGB', output_size)
    
    for index in range(grid.size_total):
        i, j = convert_index_1d_to_2d(grid, index)
        output_image.paste(
            random.choice(tiles).image,
            (i * images_size[0], j * images_size[1]),
        )
    output_image.show()


def main(images_size: Tuple[int, int], tile_prototypes: TilePrototypeMap) -> None:
    
    grid = grids.Grid2D(*(16, 9), *(False, False))
    tiles = create_tiles_from_prototypes(tile_prototypes)
    
    generate_wave_function_image(grid, tiles, images_size)


if __name__ == '__main__':
    
    main(green_knots.images_size, green_knots.tile_prototypes)
    main(circles.images_size, circles.tile_prototypes)

