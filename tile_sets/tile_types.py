from dataclasses import dataclass
from typing import Dict

import grids


class Connector():
    
    def __init__(self, style: str):
        self.style = style
    
    def __str__(self) -> str:
        return self.style


@dataclass
class Tile:
    id: str
    connectors: Dict[grids.Direction, Connector]

