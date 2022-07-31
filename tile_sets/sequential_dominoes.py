from typing import List, Tuple, cast

import grids

from . import Tile, Connector


def create(num_conn: int, cyclic: bool = False) -> Tuple[List[Connector], List[Tile]]:
    """Creates a set of 1D tiles that increments through the connections and (optionally) loops."""
    
    connectors = [cast(Connector, i) for i in range(1, num_conn + 1)]
    connectors_shifted = connectors[1:] + connectors[:1]
    
    tile_set = []
    for connector, next_connector in zip(connectors, connectors_shifted):
        
        tile_set.append(Tile(
            f'{connector}{connector}',
            {grids.Direction.LEFT: connector, grids.Direction.RIGHT: connector}),
        )
        if connector < num_conn or (cyclic and connector > 1):
            tile_set.append(Tile(
                f'{connector}{next_connector}',
                {grids.Direction.LEFT: connector, grids.Direction.RIGHT: next_connector},
            ))
    
    return connectors, tile_set

