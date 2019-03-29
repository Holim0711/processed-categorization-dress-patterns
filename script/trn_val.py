""" Training & Validation Split """

if __name__ == "__main__":
    import sys
    import math
    import random

    data = [[] for _ in range(17)]
    with open("patterns.txt") as file:
        for line in file:
            id, pat = line.split()
            data[int(pat)].append(id)

    for pat, list in enumerate(data):
        random.shuffle(list)
        for i, item in enumerate(list):
            if i < math.ceil(len(list) / 10):
                print(item, pat)
            else:
                print(item, pat, file=sys.stderr)
