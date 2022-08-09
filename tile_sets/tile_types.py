from dataclasses import dataclass
from typing import Tuple, Dict

import grids


class Connector():
    """Describes the interface a tile presents to connect with adjacent tiles."""
    
    def __init__(self, style: str):
        """Creates a simple connector that connects to itself."""
        self.style = style
        self.connects_to = {self}
    
    def __str__(self) -> str:
        return self.style
    
    def __repr__(self) -> str:
        return self.style


def create_paired_connectors(style: str) -> Tuple[Connector, Connector]:
    """Creates a pair of connectors which will only connect to each other (not themselves)."""
    
    positive, negative = Connector(f'{style} (+)'), Connector(f'{style} (-)')
    positive.connects_to = {negative}
    negative.connects_to = {positive}
    return positive, negative


@dataclass
class Tile:
    id: str
    connectors: Dict[grids.Direction, Connector]

