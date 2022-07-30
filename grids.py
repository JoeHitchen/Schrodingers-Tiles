import enum


class Direction(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'


def flip_direction(direction: Direction) -> Direction:
    """Returns the opposing direction to the one provided."""
    
    return {
        Direction.LEFT: Direction.RIGHT,
        Direction.UP: Direction.DOWN,
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWN: Direction.UP,
    }[direction]


class Grid1D():
    
    def __init__(self, size_x: int) -> None:
        self.size_x = size_x
    
    
    def get_boundary_points(self, direction: Direction) -> slice:
        return {
            Direction.LEFT: slice(0, 1),
            Direction.RIGHT: slice(self.size_x - 1, self.size_x),
        }[direction]


class Grid2D():
    
    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.size_total = size_x * size_y
    
    
    def get_boundary_points(self, direction: Direction) -> slice:
        return {
            Direction.LEFT: slice(0, self.size_total, self.size_x),
            Direction.UP: slice(0, self.size_x),
            Direction.RIGHT: slice(self.size_x - 1, self.size_total, self.size_x),
            Direction.DOWN: slice(self.size_x * (self.size_y - 1), self.size_total),
        }[direction]

