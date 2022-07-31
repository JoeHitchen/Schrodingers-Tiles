from dataclasses import dataclass
from typing import Dict, NewType

import grids


Connector = NewType('Connector', int)


@dataclass
class Tile:
    connectors: Dict[grids.Direction, Connector]

