import os
from collections import namedtuple
import csv
from pathlib import PurePath

folders = ["Italy", "Greece", "Crete", "Cyprus", "Aegean Islands", "Anatolia", "Balkans", "Gaul", "Caucasus", "Iberia", "Syria", "Mesopotamia"]
def make_path_list_from_folders(base_path, file_name):
    path_list = []
    for folder in folders:
        file_path = os.path.join(base_path, folder, file_name)
        path_list.append(file_path)
    return path_list

def get_region_from_path(path):
    p = PurePath(path)
    parts = p.parts
    region = parts[len(parts) - 2]
    return region

# CityBase
CityBase = namedtuple("CityBase", "id geonames_name geonames_cc prefix wikipedia_article_name region")

def read_city_base_files(path_list):
    city_base_list = []
    for path in path_list:
        region = get_region_from_path(path)
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                row += [region]
                city_base_list += [CityBase._make(row)]

            # city_base_list.extend([CityBase._make(x) for x in reader])
    return city_base_list


# PeriodBase
PeriodBase = namedtuple("PeriodBase", "id start_date end_date preferredName size tag_position region")

def read_period_base_files(path_list):
    period_base_list = []
    for path in path_list:
        region = get_region_from_path(path)
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                row += [region]
                period_base_list += [PeriodBase._make(row)]

            # period_base_list.extend([PeriodBase._make(x) for x in reader])
    return period_base_list


# AltNameBase
AltNameBase = namedtuple("AltNameBase", "id alt_name language region")

def read_alt_name_base_files(path_list):
    alt_name_base_list = []
    for path in path_list:
        region = get_region_from_path(path)
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                row += [region]
                alt_name_base_list += [AltNameBase._make(row)]

            # alt_name_base_list.extend([AltNameBase._make(x) for x in reader])
    return alt_name_base_list


# CityExtra
CityExtra = namedtuple("CityExtra", "id latitude longitude elevation region")

def read_city_extra_files(path_list):
    city_extra_list = []
    for path in path_list:
        region = get_region_from_path(path)
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                row += [region]
                city_extra_list += [CityExtra._make(row)]

            # city_extra_list.extend([CityExtra._make(x) for x in reader])
    return city_extra_list
