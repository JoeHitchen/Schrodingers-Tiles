from dataclasses import dataclass
from typing import Tuple, Dict

import grids


class Connector():
    
    def __init__(self, style: str):
        self.style = style
        self.connects_to = self
    
    def __str__(self) -> str:
        return self.style
    
    def __repr__(self) -> str:
        return self.style


def create_paired_connectors(style: str) -> Tuple[Connector, Connector]:
    positive, negative = Connector(f'{style}+'), Connector(f'{style}-')
    positive.connects_to = negative
    negative.connects_to = positive
    return positive, negative


@dataclass
class Tile:
    id: str
    connectors: Dict[grids.Direction, Connector]

