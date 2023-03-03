import csv, os

import pandas as pd

path = os.path.abspath(os. path. dirname(__file__))

directory = path + "/../raw_data"

iso_dict = {}

with open(path + "/iso.csv", 'r') as csvfile:
    next(csvfile) # Skip the header row.
    datareader = csv.reader(csvfile)
    for row in datareader:
        iso_dict[row[0]] = row[1]

region_id_map = {
    "South America": 0,
    "Antarctica": 1,
    "South Asia": 2,
    "Europe": 3,
    "Australia and Oceania": 4,
    "Central Asia": 5,
    "Central America and the Caribbean": 6,
    "Africa": 7,
    "East and Southeast Asia": 8,
    "Middle East": 9,
    "North America": 10
}

# id, name, region_id
with open(path + "/countries.csv", 'r') as csvfile:
    content = []
    next(csvfile)

    datareader = csv.reader(csvfile)
    for row in datareader:
        # print([row[0], row[1], row[2]])
        if row[0] in iso_dict and row[2] in region_id_map:
            content.append([iso_dict[row[0]], row[0], region_id_map[row[2]]])

    df = pd.DataFrame(content)
    df.to_csv(path + "/../formatted_data/" + "processed_countries.csv", index=False, header=False)


with open(path + "/iso.csv", 'r') as csvfile:
    next(csvfile) # Skip the header row.
    datareader = csv.reader(csvfile)
    for row in datareader:
        iso_dict[row[0]] = row[1]
 
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
        
        # convert 3rd column (value) to float
        for row in content:
            if row[2] != '':
                row[2] = float(row[2].replace(',',''))
            else:
                row[2] = None

        # set non-numeric values to null in first column (date)
        for row in content:
            try:
                int(row[0])
            except ValueError:
                row[0] = 2023


    df = pd.DataFrame(content)
    df.to_csv(path + "/../formatted_data/" + "processed_" + filename, index=False, header=False)
