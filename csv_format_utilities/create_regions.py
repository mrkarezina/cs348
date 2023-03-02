import csv, os

import pandas as pd


path = os.path.abspath(os. path. dirname(__file__))

regions = set()

with open(path + "./countries.csv", 'r') as csvfile:
    next(csvfile) # Skip the header row.
    datareader = csv.reader(csvfile)
    for row in datareader:
        regions.add(row[2])


df = pd.DataFrame(list(regions), columns=['name'])
df.to_csv(path + "/regions.csv", index=True)

