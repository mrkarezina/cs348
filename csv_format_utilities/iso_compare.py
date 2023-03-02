import csv, os, sys

path = os.path.abspath(os. path. dirname(__file__))

iso_dict = {}

with open(path + "./iso.csv", 'r') as csvfile:
    next(csvfile) # Skip the header row.
    datareader = csv.reader(csvfile)
    for row in datareader:
        iso_dict[row[0]] = row[1]

unused_iso = iso_dict.copy()

countries = []

with open(path + "./countries.csv", 'r') as csvfile:
    next(csvfile) # Skip the header row.
    datareader = csv.reader(csvfile)
    for row in datareader:
        countries.append(row[0])

unmatched_countries = countries.copy()

used_isos = {}

for country in countries:
    if country in unused_iso:
        used_isos[unused_iso[country]] = country
        unused_iso.pop(country)
        unmatched_countries.remove(country)
        

    else:
        if country in iso_dict:
            print("wtf?")
            sys.exit()

print(unused_iso)
print("_____________________________________________________________________________________________")
print(unmatched_countries)
print("_____________________________________________________________________________________________")
print(used_isos)
print(len(used_isos))