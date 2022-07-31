from dataclasses import dataclass
from typing import Dict

import grids


@dataclass
class Tile:
    connectors: Dict[grids.Direction, int]

