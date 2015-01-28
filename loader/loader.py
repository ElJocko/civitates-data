import csv
import json
import os
from collections import namedtuple

print("civitates-data loader starting")

# TBD: Read the data locations from a file
base_path = "../data"
city_base_files = ["Italy/CityBase.txt", "Greece/CityBase.txt"]
period_base_files = ["Italy/PeriodBase.txt", "Greece/PeriodBase.txt"]
alt_name_base_files = ["Italy/AltNameBase.txt", "Greece/AltNameBase.txt"]
city_extra_files = ["Italy/CityExtra.txt"]

# Read geonames file
GeonamesCity = namedtuple("GeonamesCity", "city_id name ascii_name alternate_names latitude longitude feature_class feature_code country_code cc2 admin_code1 admin_code2 admin_code3 admin_code4 population elevation dem time_zone modification_date")
with open("../data/cities1000.txt", encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    geonames_city_list = [GeonamesCity._make(x) for x in reader]

print("Read", len(geonames_city_list), "rows from cities1000.txt")

# Read CityBase files
CityBase = namedtuple("CityBase", "id geonames_name geonames_cc prefix")
city_base_list = []
for filename in city_base_files:
    file_path = os.path.join(base_path, filename)
    with open(file_path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        city_base_list.extend([CityBase._make(x) for x in reader])

print("Read", len(city_base_list), "rows from CityBase.txt")

def count_id(id, list):
    count = 0
    for x in list:
        if x.id == id:
            count += 1
    return count

# Read PeriodBase.txt
PeriodBase = namedtuple("PeriodBase", "id start_date end_date preferredName size tag_position")
period_base_list = []
for filename in period_base_files:
    file_path = os.path.join(base_path, filename)
    with open(file_path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        period_base_list.extend([PeriodBase._make(x) for x in reader])

print("Read", len(period_base_list), "rows from PeriodBase.txt")

# Read AltNameBase.txt
AltNameBase = namedtuple("AltNameBase", "id alt_name language")
alt_name_base_list = []
for filename in alt_name_base_files:
    file_path = os.path.join(base_path, filename)
    with open(file_path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        alt_name_base_list.extend([AltNameBase._make(x) for x in reader])

print("Read", len(alt_name_base_list), "rows from AltNamedBase.txt")

# Read CityExtra.txt
CityExtra = namedtuple("CityExtra", "id latitude longitude elevation")
city_extra_list = []
for filename in city_extra_files:
    file_path = os.path.join(base_path, filename)
    with open(file_path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        city_extra_list.extend([CityExtra._make(x) for x in reader])

print("Read", len(city_extra_list), "rows from CityExtra.txt")

# Look for duplicates in CityBase
duplicate_cities = set([x.id for x in city_base_list if count_id(x.id, city_base_list) > 1])
if len(duplicate_cities) > 1:
    print("Found", len(duplicate_cities), "duplicate cities in CityExtra.txt")
    for duplicate in duplicate_cities:
        print("  ", duplicate)

def find_geonames_city(name):
    for city in geonames_city_list:
        if city.name == name:
            return city
    return None

def find_city_extra(city_id):
    for city in city_extra_list:
        if city.id == city_id:
            return city
    return None

def get_alt_names(city_id):
    city_alt_names = []
    for alt_name in alt_name_base_list:
        if alt_name.id == city_id:
            city_alt_names.append({ 'name':alt_name.alt_name, 'language':alt_name.language })
    return city_alt_names

def get_city_periods(city_id):
    city_periods = []
    for period in period_base_list:
        if period.id == city_id:
            city_periods.append({ 'startDate':period.start_date, 'endDate':period.end_date, 'preferredName':period.preferredName, 'size':period.size, 'tagPosition':period.tag_position })
    return city_periods

# Write the cities to the JSON output file
city_list = []
for city_base in city_base_list:
    geonames_city = find_geonames_city(city_base.geonames_name)
    if geonames_city is None:
        geonames_city = find_city_extra(city_base.id)

    if geonames_city is None:
        print("No geo information found for ", city_base.id)
        continue

    alt_names = get_alt_names(city_base.id)
    periods = get_city_periods(city_base.id)
    city = { 'identifier':city_base.id,
             'latitude':geonames_city.latitude,
             'longitude':geonames_city.longitude,
             'elevation':geonames_city.elevation,
             'prefix':city_base.prefix,
             'periods': periods,
             'altNames': alt_names }
    city_list.append(city)

filename = '../data/city-test.json'
with open(filename, 'w') as file:
    json.dump(city_list, file, indent=4, separators=(',', ': ') )

print("Wrote", len(city_list), "cities to", filename)
