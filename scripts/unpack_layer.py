from scripts.unpack_column import unpack_column


def unpack_layer(path: str) -> list:
    layer = [i for i in unpack_column(path)]
    return layer
