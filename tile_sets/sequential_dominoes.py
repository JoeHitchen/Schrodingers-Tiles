import grids

from . import Tile, Connector, create_paired_connectors


def create(
    num_conn: int,
    cyclic: bool = False,
    polarised: bool = False,
) -> tuple[list[Connector], list[Tile]]:
    """Creates a set of 1D tiles that increments through the connections and (optionally) loops."""

    def create_unpolarised_connectors(style: str) -> tuple[Connector, Connector]:
        return 2 * (Connector(style),)

    connector_function = create_paired_connectors if polarised else create_unpolarised_connectors

    connector_numbers = range(1, num_conn + 1)
    connector_pairs = [connector_function(str(i)) for i in connector_numbers]
    left_connectors = [left for left, right in connector_pairs]
    right_connectors = [right for _, right in connector_pairs]
    next_right_connectors = right_connectors[1:] + right_connectors[:1]

    tile_set = []
    iterator = zip(connector_numbers, left_connectors, right_connectors, next_right_connectors)
    for number, left_connector, right_connector, next_right_connector in iterator:

        tile_set.append(Tile(
            f'{left_connector}/{right_connector}',
            {grids.Direction.LEFT: left_connector, grids.Direction.RIGHT: right_connector}),
        )
        if number < num_conn:
            tile_set.append(Tile(
                f'{left_connector}/{next_right_connector}',
                {
                    grids.Direction.LEFT: left_connector,
                    grids.Direction.RIGHT: next_right_connector,
                },
            ))
        elif cyclic and number > 1:
            tile_set.append(Tile(
                f'{left_connector}/{next_right_connector}',
                {
                    grids.Direction.LEFT: left_connector,
                    grids.Direction.RIGHT: next_right_connector,
                },
            ))

    all_connectors: list[Connector] = []
    for connector_pair in connector_pairs:
        all_connectors.extend(connector_pair)
    return all_connectors, tile_set

