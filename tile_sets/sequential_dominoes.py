from typing import List, cast

import grids

from . import Tile, Connector


def create(num_conn: int, cyclic: bool = False) -> List[Tile]:
    """Creates a set of 1D tiles that increments through the connections and (optionally) loops."""
    
    tile_set = []
    for i in range(1, num_conn + 1):
        
        c1 = cast(Connector, 1)
        ci = cast(Connector, i)
        cn = cast(Connector, i + 1)
        
        tile_set.append(Tile(
            f'{ci}{ci}',
            {grids.Direction.LEFT: ci, grids.Direction.RIGHT: ci}),
        )
        if i < num_conn:
            tile_set.append(Tile(
                f'{ci}{cn}',
                {grids.Direction.LEFT: ci, grids.Direction.RIGHT: cn},
            ))
        elif cyclic and i > 1:
            tile_set.append(Tile(
                f'{ci}{c1}',
                {grids.Direction.LEFT: ci, grids.Direction.RIGHT: c1},
            ))
    
    return tile_set

