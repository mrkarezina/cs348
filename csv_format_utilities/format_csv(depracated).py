import csv, os

import pandas as pd

path = os.path.abspath(os. path. dirname(__file__))


iso_dict = {}

with open(path + "/iso.csv", 'r') as csvfile:
    next(csvfile) # Skip the header row.
    datareader = csv.reader(csvfile)
    for row in datareader:
        iso_dict[row[0]] = row[1]


directory = path + "/../raw_data"
 
# iterate over files in raw_data
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)

    print(filename)

    content = []

    with open(f, 'r') as csvfile:
        next(csvfile) # Skip the header row.
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[0] in iso_dict:
                date = row[3][0:4] if row[3] != '' else row[3]
                content.append([date, iso_dict[row[0]], row[2]])

    df = pd.DataFrame(content)
    df.to_csv(path + "/../services/web/data/" + filename, index=False)
            