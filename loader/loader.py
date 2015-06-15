import csv
import json
import os
from collections import namedtuple

print("civitates-data loader starting")

# TBD: Read the data locations from a file
base_path = "../data"

output_filename = "City.json"
geonames_filename = "cities1000.txt"
pleiades_filename = "pleiades-places.csv"

folders = ["Italy", "Greece", "Crete", "Cyprus", "Aegean Islands"]

# Read geonames file
GeonamesCity = namedtuple("GeonamesCity", "city_id name ascii_name alternate_names latitude longitude feature_class feature_code country_code cc2 admin_code1 admin_code2 admin_code3 admin_code4 population elevation dem time_zone modification_date")
geonames_path = os.path.join(base_path, geonames_filename)
with open(geonames_path, encoding="utf8") as file:
    reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    geonames_city_list = [GeonamesCity._make(x) for x in reader]

print("Read", len(geonames_city_list), "rows from", geonames_filename)

# Read Pleiades Places file
PleiadesPlace = namedtuple("PleiadesPlace", "authors bbox connects_with created creators current_version description extent feature_types geo_context has_connections_with id location_precision max_date min_date modified path repr_lat repr_lat_long repr_long tags time_periods time_periods_keys time_periods_range title uid")
pleiades_path = os.path.join(base_path, pleiades_filename)
with open(pleiades_path, encoding="utf8") as file:
    reader = csv.reader(file, delimiter=',')
    next(reader) # skip the header row
    pleiades_place_list = [PleiadesPlace._make(x) for x in reader]

print("Read", len(pleiades_place_list), "rows from", pleiades_filename)

PleiadesSettlement = namedtuple("PleiadesSettlement", "title latitude longitude elevation")
pleiades_settlement_list = []
for place in pleiades_place_list:
    if "settlement" in place.feature_types:
        settlement = PleiadesSettlement(place.title, place.repr_lat, place.repr_long, 0)
        pleiades_settlement_list.append(settlement)

print("Found", len(pleiades_settlement_list), "settlements")

# Read CityBase files
file_name = "CityBase.txt"
CityBase = namedtuple("CityBase", "id geonames_name geonames_cc prefix")
city_base_list = []
for folder in folders:
    file_path = os.path.join(base_path, folder, file_name)
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
file_name = "PeriodBase.txt"
for folder in folders:
    file_path = os.path.join(base_path, folder, file_name)
    with open(file_path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        period_base_list.extend([PeriodBase._make(x) for x in reader])

print("Read", len(period_base_list), "rows from PeriodBase.txt")

# Read AltNameBase.txt
AltNameBase = namedtuple("AltNameBase", "id alt_name language")
alt_name_base_list = []
file_name = "AltNameBase.txt"
for folder in folders:
    file_path = os.path.join(base_path, folder, file_name)
    with open(file_path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        alt_name_base_list.extend([AltNameBase._make(x) for x in reader])

print("Read", len(alt_name_base_list), "rows from AltNamedBase.txt")

# Read CityExtra.txt
CityExtra = namedtuple("CityExtra", "id latitude longitude elevation")
city_extra_list = []
file_name = "CityExtra.txt"
for folder in folders:
    file_path = os.path.join(base_path, folder, file_name)
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

def find_geonames_city(name, country_code):
    for city in geonames_city_list:
        if city.ascii_name == name and city.country_code == country_code:
            return city
    return None

def find_pleiades_settlement(title):
    for settlement in pleiades_settlement_list:
        if settlement.title == title:
            print("  found", title, "in pleiades settlements")
            return settlement
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
    city_lookup = None
    if city_base.geonames_cc == "P":
        city_lookup = find_pleiades_settlement(city_base.geonames_name)

    if city_lookup is None:
        city_lookup = find_geonames_city(city_base.geonames_name, city_base.geonames_cc)

    if city_lookup is None:
        city_lookup = find_city_extra(city_base.id)

    if city_lookup is None:
        print("No geo information found for ", city_base.id)
        continue

    alt_names = get_alt_names(city_base.id)
    periods = get_city_periods(city_base.id)
    city = { 'identifier':city_base.id,
             'latitude':city_lookup.latitude,
             'longitude':city_lookup.longitude,
             'elevation':city_lookup.elevation,
             'prefix':city_base.prefix,
             'periods': periods,
             'altNames': alt_names }
    city_list.append(city)

output_object = { 'cities': city_list }
output_path = os.path.join(base_path, output_filename)
with open(output_path, 'w') as file:
    json.dump(output_object, file, indent=4, separators=(',', ': ') )

print("Wrote", len(city_list), "cities to", output_filename)
