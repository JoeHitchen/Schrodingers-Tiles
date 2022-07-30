import tiles


class Grid1D():
    
    def __init__(self, size_x: int) -> None:
        self.size_x = size_x
    
    
    def get_boundary_points(self, direction: tiles.Directions) -> slice:
        return {
            tiles.Directions.LEFT: slice(0, 1),
            tiles.Directions.RIGHT: slice(self.size_x - 1, self.size_x),
        }[direction]


class Grid2D():
    
    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.size_total = size_x * size_y
    
    
    def get_boundary_points(self, direction: tiles.Directions) -> slice:
        return {
            tiles.Directions.LEFT: slice(0, self.size_total, self.size_x),
            tiles.Directions.UP: slice(0, self.size_x),
            tiles.Directions.RIGHT: slice(self.size_x - 1, self.size_total, self.size_x),
            tiles.Directions.DOWN: slice(self.size_x * (self.size_y - 1), self.size_total),
        }[direction]

