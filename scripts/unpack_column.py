def unpack_column(path: str) -> list:
    with open(path) as file:
        column = []
        row = file.readline()
        while row != "":
            column.append(row.strip())
            row = file.readline()
        return column
