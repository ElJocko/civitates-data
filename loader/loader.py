import json
import os
from collections import namedtuple
from dataclasses import dataclass
import labelCalc
import geonames
import pleiades
import civitates_data


def count_id(city, list):
    count = 0
    for x in list:
        if x.id == city.id and x.region == city.region:
            count += 1
    return count

def find_geonames_city(name, country_code):
    for city in geonames_city_list:
        if city.ascii_name == name and city.country_code == country_code:
            return city
    return None

def find_pleiades_settlement(title):
    for settlement in pleiades_settlement_list:
        if settlement.title == title:
            # print("  found", title, "in pleiades settlements")
            return settlement
    return None

def find_city_extra(city_id, region):
    for city in city_extra_list:
        if city.id == city_id and city.region == region:
            return city
    return None

def get_alt_names(city_id, region):
    city_alt_names = []
    for alt_name in alt_name_base_list:
        if alt_name.id == city_id and alt_name.region == region:
            city_alt_names.append({ 'name':alt_name.alt_name, 'language':alt_name.language })
    return city_alt_names

def get_city_periods(city_id, region):
    city_periods = []
    for period in period_base_list:
        if period.id == city_id and period.region == region:
            city_periods.append({ 'startDate':period.start_date, 'endDate':period.end_date, 'preferredName':period.preferredName, 'size':period.size, 'tagPosition':period.tag_position, 'calcTagPosition':0 })
    return city_periods


print("civitates-data loader starting")

# TBD: Read the data locations from a file
base_path = "../data"

output_filename = "City.json"
geonames_filename = "cities1000.txt"
pleiades_filename = "pleiades-places.csv"

# Read geonames file
geonames_path = os.path.join(base_path, geonames_filename)
geonames_city_list = geonames.read_geonames_city_file(geonames_path)

print("Read", len(geonames_city_list), "rows from", geonames_filename)

# Read Pleiades Places file
pleiades_path = os.path.join(base_path, pleiades_filename)
pleiades_place_list = pleiades.read_pleiades_place_file(pleiades_path)

print("Read", len(pleiades_place_list), "rows from", pleiades_filename)

# Filter for settlements and convert to common form
PleiadesSettlement = namedtuple("PleiadesSettlement", "title latitude longitude elevation")
pleiades_settlement_list = []
for place in pleiades_place_list:
    if "settlement" in place.feature_types:
        settlement = PleiadesSettlement(place.title, place.repr_lat, place.repr_long, "0")
        pleiades_settlement_list.append(settlement)

print("Found", len(pleiades_settlement_list), "settlements")

# Read CityBase files
path_list = civitates_data.make_path_list_from_folders(base_path, "CityBase.txt")
city_base_list = civitates_data.read_city_base_files(path_list)

print("Read", len(city_base_list), "rows from CityBase.txt")

# Read PeriodBase.txt
path_list = civitates_data.make_path_list_from_folders(base_path, "PeriodBase.txt")
period_base_list = civitates_data.read_period_base_files(path_list)

print("Read", len(period_base_list), "rows from PeriodBase.txt")

# Read AltNameBase.txt
path_list = civitates_data.make_path_list_from_folders(base_path, "AltNameBase.txt")
alt_name_base_list = civitates_data.read_alt_name_base_files(path_list)

print("Read", len(alt_name_base_list), "rows from AltNamedBase.txt")

# Read CityExtra.txt
path_list = civitates_data.make_path_list_from_folders(base_path, "CityExtra.txt")
city_extra_list = civitates_data.read_city_extra_files(path_list)

print("Read", len(city_extra_list), "rows from CityExtra.txt")

# Look for duplicates in CityBase
duplicate_cities = set([x.id for x in city_base_list if count_id(x, city_base_list) > 1])
if len(duplicate_cities) > 0:
    print("Found", len(duplicate_cities), "duplicate cities in CityBase.txt")
    for duplicate in duplicate_cities:
        print("  ", duplicate)

# Write the cities to the JSON output file
city_list = []
for city_base in city_base_list:
    city_lookup = None
    if city_base.geonames_cc == "P":
        city_lookup = find_pleiades_settlement(city_base.geonames_name)
    elif city_base.geonames_cc == "X":
        city_lookup = find_city_extra(city_base.id, city_base.region)

    if city_lookup is None:
        city_lookup = find_geonames_city(city_base.geonames_name, city_base.geonames_cc)

    if city_lookup is None:
        city_lookup = find_city_extra(city_base.id, city_base.region)

    if city_lookup is None:
        print("No geo information found for", city_base.id, " (", city_base.region, ")")
        continue

    alt_names = get_alt_names(city_base.id, city_base.region)
    periods = get_city_periods(city_base.id, city_base.region)
    map_point = labelCalc.map_point_for_coordinate(labelCalc.Coordinate(city_lookup.latitude, city_lookup.longitude))

    #city = City(city_base.id)

    city_dict = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [ city_lookup.longitude, city_lookup.latitude]
        },
        'properties': {
            'identifier': city_base.id + "@" + city_base.region,
            'city_base_id': city_base.id,
            'region': city_base.region,
            'latitude': city_lookup.latitude,
            'longitude': city_lookup.longitude,
            'elevation': city_lookup.elevation,
            'prefix': city_base.prefix,
            'periods': periods,
            'altNames': alt_names,
            'mapPoint': map_point,
            'wikipediaArticleName': city_base.wikipedia_article_name
        }}
    city_list.append(city_dict)



@dataclass
class CityPeriodCalc:
    id: str
    start_date: int
    end_date: int
    marker_rect: labelCalc.ScreenRect
    tag_rect: labelCalc.ScreenRect
    city_period: dict

@dataclass
class CityCalc:
    id: str
    max_size: int
    size_duration: int
    periods: list


def build_city_period_screen_locs(zoom_level, year):
    # Screen locations for each city size
    screen_locs = [ [], [], [], [], [] ]

    for city in city_list:
        for period in city["properties"]["periods"]:
            start_date = int(period["startDate"])
            end_date = int(period["endDate"])
            if (start_date <= year and end_date >= year):
                # Period overlaps target year
                marker_rect = labelCalc.marker_screen_rect_for_map_point(city["properties"]["mapPoint"], zoom_level)
                tag_rect = labelCalc.tag_screen_rect_for_map_point(city["properties"]["mapPoint"], period["calcTagPosition"], zoom_level)
                city_period = CityPeriodCalc(city["properties"]["identifier"], period["startDate"], period["endDate"], marker_rect, tag_rect, period)
                screen_locs[int(period["size"])].append(city_period)

    return screen_locs

def check_cities_overlap(cities0, cities1):
    overlap_found = False
    for city0 in cities0:
        for city1 in cities1:
            if city0.id != city1.id:
                if labelCalc.screen_rects_overlap(city0.marker_rect, city1.tag_rect):
                    print("    ** overlap ** ", city0.id, " with ", city1.id)
                    if city1.city_period["calcTagPosition"] < 7:
                        city1.city_period["calcTagPosition"] += 1
                    else:
                        print("Unable to find position for ", city1.id, " tag")
                    overlap_found = True
    return overlap_found


def count_cities_by_size(cities):
    count = [0, 0, 0, 0, 0]
    for city in cities:
        city_periods = city["properties"]["periods"]

        if len(city_periods) == 0:
            print("  no periods entered for ", city["properties"]["city_base_id"])
        else:
            min_period = min(city_periods, key=lambda x: x["size"])
            city_size = int(min_period["size"])
            count[city_size] = count[city_size] + 1

    print("City sizes:")
    for size in range(0, 5):
        print("  size ", size, ": ", count[size])


def min_size_for_zoom_level(zoom_level):
    zoom_threshholds = [0.0, 5.0, 6.0, 7.0, 8.0]
    min_size = -1
    for threshold in zoom_threshholds:
        if zoom_level >= threshold:
            min_size = min_size + 1

    return min_size


for year in [-500, -250, -100, 100, 250, 500, 1000]:
    print("Checking year ", year)
    for zoom_level in [2.5, 5.5, 6.5, 7.5, 8.5]:
        screen_locs = build_city_period_screen_locs(zoom_level, year)
        # print("Checking overlap for zoom level ", zoom_level)
        min_size = min_size_for_zoom_level(zoom_level)
        for i in range(0, min_size + 1):
            for j in range(i, min_size + 1):
                # print("Checking size ", i, " and ", j)
                overlap_found = False
                while overlap_found:
                    overlap_found = check_cities_overlap(screen_locs[i], screen_locs[j])
                    if overlap_found:
                        # print("Recalculating screen locs")
                        screen_locs = build_city_period_screen_locs(zoom_level, year)


#check_cities_overlap(screen_locs[0], screen_locs[0])
#check_cities_overlap(screen_locs[0], screen_locs[1])
#check_cities_overlap(cities[0], cities[2])
#check_cities_overlap(cities[0], cities[3])
#check_cities_overlap(cities[1], cities[2])
#check_cities_overlap(cities[1], cities[3])
#check_cities_overlap(cities[2], cities[3])

count_cities_by_size(city_list)

output_object = { 'type': 'FeatureCollection', 'crs': { 'type': 'name', 'properties': { 'name': 'EPSG:4326' }}, 'features': city_list }
output_path = os.path.join(base_path, output_filename)
with open(output_path, 'w') as file:
    json.dump(output_object, file, indent=4, separators=(',', ': ') )

print("Wrote", len(city_list), "cities to", output_filename)
