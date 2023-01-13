import csv
def unpack_csv(path, delimiter):
    with open(path) as f:
        data = csv.reader(f,delimiter=delimiter)
        res = []
        for i in data:
            # print(i)
            res.append(i)
    return res