from tile_sets.image_tiles import TilePrototypeMap, create_tiles_from_prototypes
from tile_sets import green_knots, circles


def main(tile_prototypes: TilePrototypeMap) -> None:
    
    tiles = create_tiles_from_prototypes(tile_prototypes)
    for tile in tiles:
        print(tile)
        print(tile.image)
        tile.image.show()


if __name__ == '__main__':
    
    main(green_knots.tile_prototypes)
    main(circles.tile_prototypes)

