"""
import json
with open('features.json') as f: a = json.load(f)
name_to_iso = {}
for geo in a['objects']['world']['geometries']:
    name_to_iso[geo['properties']['name']] = geo['id']

for geo in b['objects']['countries']['geometries']:
    name = geo['properties']['name']
    if name not in name_to_iso: print(name)
    else: geo['id'] = name_to_iso[name]
"""

import requests
import json

FILE = 'countries-50m.json'

url = 'https://restcountries.com/v2/name/'

with open(FILE, encoding='utf-8') as f:
    b = json.load(f)
for geo in b['objects']['countries']['geometries']:
    name = geo['properties']['name']
    if 'Is.' in name:
        name = geo['properties']['name'] = name.replace('Is.', 'Islands')
    if 'St.' in name:
        name = geo['properties']['name'] = name.replace('St.', 'Saint')
    if 'St-' in name:
        name = geo['properties']['name'] = name.replace('St-', 'Saint ')
    if 'N.' in name:
        name = geo['properties']['name'] = name.replace('"N. ', '"Northern ')
        name = geo['properties']['name'] = name.replace(' N. ', ' Northern ')
    if 'W.' in name:
        name = geo['properties']['name'] = name.replace('"W. ', '"Western ')
        name = geo['properties']['name'] = name.replace(' W. ', ' Western ')
    if 'Ter.' in name:
        name = geo['properties']['name'] = name.replace('Ter.', 'Territory')
    if 'Fr.' in name:
        name = geo['properties']['name'] = name.replace('Fr.', 'French')
    if 'Eq.' in name:
        name = geo['properties']['name'] = name.replace('Eq.', 'Equatorial ')
    if 'Rep.' in name:
        name = geo['properties']['name'] = name.replace('Rep.', 'Republic')
    if 'I.' in name:
        name = geo['properties']['name'] = name.replace('I.', 'Island')
    _id = geo['properties'].pop('id', None)
    try:
        if _id is None:
            _id = geo['id']
        if _id.isnumeric():
            r = requests.get(url + name)
            if r.status_code == 404:
                print(name, f'({_id}) could not be found')
            else:
                alpha3Code = r.json()[0]['alpha3Code']
                geo['id'] = alpha3Code
        else:
            geo['id'] = _id
    except (KeyError, AttributeError):
        if _id is not None:
            geo['id'] = _id

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(b, f, indent=4)
# with open('countries.txt', encoding='utf-8') as f:
#     for line in f.readlines():
#         line = line.strip()
