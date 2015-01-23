import csv
import json
from collections import namedtuple

print("civitates-data loader starting")

# Read geonames file
GeonamesCity = namedtuple("GeonamesCity", "city_id name ascii_name alternate_names latitude longitude feature_class feature_code country_code cc2 admin_code1 admin_code2 admin_code3 admin_code4 population elevation dem time_zone modification_date")
with open("..\data\cities1000.txt", encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    geonames_city_list = [GeonamesCity._make(x) for x in reader]

print("Read", len(geonames_city_list), "rows from cities1000.txt")

# Read CityBase.txt
CityBase = namedtuple("CityBase", "id geonames_name geonames_cc prefix")
with open("..\data\CityBase.txt", encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    city_base_list = [CityBase._make(x) for x in reader]

print("Read", len(city_base_list), "rows from CityBase.txt")

def count_id(id, list):
    count = 0
    for x in list:
        if x.id == id:
            count += 1
    return count

# Read PeriodBase.txt
PeriodBase = namedtuple("PeriodBase", "id start_date end_date preferredName size tag_position")
with open("..\data\PeriodBase.txt", encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    period_base_list = [PeriodBase._make(x) for x in reader]

print("Read", len(period_base_list), "rows from PeriodBase.txt")

# Read AltNameBase.txt
AltNameBase = namedtuple("AltNameBase", "id alt_name language")
with open("..\data\AltNameBase.txt", encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    alt_name_base_list = [AltNameBase._make(x) for x in reader]

print("Read", len(alt_name_base_list), "rows from AltNamedBase.txt")

# Read CityExtra.txt
CityExtra = namedtuple("CityExtra", "id latitude longitude elevation")
with open("..\data\CityExtra.txt", encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    city_extra_list = [CityExtra._make(x) for x in reader]

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

def find_city_extra(id):
    for city in city_extra_list:
        if city.id == id:
            return city
    return None

# Write the cities to the JSON output file
for city_base in city_base_list:
    geonames_city = find_geonames_city(city_base.geonames_name)
    if geonames_city is None:
        geonames_city = find_city_extra(city_base.id)

    if geonames_city is None:
        print("No geo information found for ", city_base.id)
        continue

    print(json.dumps( { 'identifier':city_base.id, 'latitude':geonames_city.latitude, 'longitude':geonames_city.longitude, 'elevation':geonames_city.elevation, 'prefix':city_base.prefix }, sort_keys=True, indent=4, separators=(',', ': ') ))
