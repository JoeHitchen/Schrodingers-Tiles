from typing import Tuple
import random

from PIL import Image as pillow
from tile_sets.image_tiles import TilePrototypeMap, create_tiles_from_prototypes
from tile_sets import Connector, green_knots, circles
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


def main(
    images_size: Tuple[int, int],
    tile_prototypes: TilePrototypeMap,
    boundary_connector: Connector,
    cyclic: bool = False,
) -> None:
    
    grid = grids.Grid2D(*(16, 9), *(cyclic, cyclic))
    tiles = create_tiles_from_prototypes(tile_prototypes)
    
    wave_function = wave_functions.WaveFunction(grid, tiles)
    if not cyclic:
        for direction in grids.Direction:
            wave_function.apply_boundary_constraint(direction, {boundary_connector})
    
    while not wave_function.collapsed:
        cell = wave_function.get_most_constrained_cell()
        tile = random.choice(cell.state)
        print(f'Selected [{tile.id}] in {cell}')
        cell.tile = tile
    
    generate_wave_function_image(wave_function, images_size)


if __name__ == '__main__':
    
    main(
        green_knots.images_size,
        green_knots.tile_prototypes,
        green_knots.boundary_connector,
        cyclic = False,
    )
    main(
        circles.images_size,
        circles.tile_prototypes,
        circles.boundary_connector,
        cyclic = True,
    )

