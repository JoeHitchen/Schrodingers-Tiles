from typing import List, Tuple, Protocol
import enum


class Direction(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

    def __repr__(self) -> str:
        return self.value


def flip_direction(direction: Direction) -> Direction:
    """Returns the opposing direction to the one provided."""

    return {
        Direction.LEFT: Direction.RIGHT,
        Direction.UP: Direction.DOWN,
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWN: Direction.UP,
    }[direction]


class Grid(Protocol):

    size_x: int
    size_y: int
    size_total: int
    cyclic_x: bool
    cyclic_y: bool

    def make_cell_id(self, index: int) -> str:
        pass

    def get_boundary_slice(self, direction: Direction) -> slice:
        pass

    def get_neighbour_slices(self) -> List[Tuple[slice, Direction, bool]]:
        pass


class Grid1D():

    def __init__(self, size_x: int, cyclic_x: bool) -> None:
        self.size_x = size_x
        self.size_y = 1
        self.size_total = size_x
        self.cyclic_x = cyclic_x
        self.cyclic_y = False


    def make_cell_id(self, index: int) -> str:
        return str(index + 1)


    def get_boundary_slice(self, direction: Direction) -> slice:
        return {
            Direction.LEFT: slice(0, 1),
            Direction.RIGHT: slice(self.size_x - 1, self.size_x),
        }[direction]


    def get_neighbour_slices(self) -> List[Tuple[slice, Direction, bool]]:
        return [(slice(0, self.size_x), Direction.RIGHT, self.cyclic_x)]


class Grid2D():

    def __init__(self, size_x: int, size_y: int, cyclic_x: bool, cyclic_y: bool) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.size_total = size_x * size_y

        self.cyclic_x = cyclic_x
        self.cyclic_y = cyclic_y


    def make_cell_id(self, index: int) -> str:
        x_pos = index % self.size_x
        y_pos = (index - x_pos) // self.size_x
        return f'{x_pos + 1}-{y_pos + 1}'


    def get_boundary_slice(self, direction: Direction) -> slice:
        return {
            Direction.LEFT: slice(0, self.size_total, self.size_x),
            Direction.UP: slice(0, self.size_x),
            Direction.RIGHT: slice(self.size_x - 1, self.size_total, self.size_x),
            Direction.DOWN: slice(self.size_x * (self.size_y - 1), self.size_total),
        }[direction]


    def get_neighbour_slices(self) -> List[Tuple[slice, Direction, bool]]:
        horizontal_neighbours = [
            (slice(self.size_x * j, self.size_x * (j + 1)), Direction.RIGHT, self.cyclic_x)
            for j in range(self.size_y)
        ]
        vertical_neighbours = [
            (slice(i, self.size_total, self.size_x), Direction.DOWN, self.cyclic_y)
            for i in range(self.size_x)
        ]
        return horizontal_neighbours + vertical_neighbours

