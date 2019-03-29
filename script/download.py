""" Download original images

"dress_patterns.csv" is the original txt data.
From that, download original images.
"""
import sys
import csv
from tqdm import tqdm
from urllib.request import urlretrieve

with open("dress_patterns.csv") as file:
    reader = csv.reader(file)

    header = reader.__next__()

    for row in tqdm(reader):
        uid = row[0]
        url = row[-1]
        try:
            urlretrieve(url, "image/%s.png" % uid)
        except Exception:
            print(row, file=sys.stderr)
