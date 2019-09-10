from collections import namedtuple
import csv

GeonamesCity = namedtuple("GeonamesCity", "city_id name ascii_name alternate_names latitude longitude feature_class feature_code country_code cc2 admin_code1 admin_code2 admin_code3 admin_code4 population elevation dem time_zone modification_date")

def read_geonames_city_file(path):
    with open(path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        geonames_city_list = [GeonamesCity._make(x) for x in reader]
        return geonames_city_list
