import os
from collections import namedtuple
import csv

folders = ["Italy", "Greece", "Crete", "Cyprus", "Aegean Islands", "Anatolia", "Balkans", "Gaul", "Caucasus", "Iberia", "Syria", "Mesopotamia"]
def make_path_list_from_folders(base_path, file_name):
    path_list = []
    for folder in folders:
        file_path = os.path.join(base_path, folder, file_name)
        path_list.append(file_path)
    return path_list


# CityBase
CityBase = namedtuple("CityBase", "id geonames_name geonames_cc prefix wikipedia_article_name")

def read_city_base_files(path_list):
    city_base_list = []
    for path in path_list:
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            city_base_list.extend([CityBase._make(x) for x in reader])
    return city_base_list


# PeriodBase
PeriodBase = namedtuple("PeriodBase", "id start_date end_date preferredName size tag_position")

def read_period_base_files(path_list):
    period_base_list = []
    for path in path_list:
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            period_base_list.extend([PeriodBase._make(x) for x in reader])
    return period_base_list


# AltNameBase
AltNameBase = namedtuple("AltNameBase", "id alt_name language")

def read_alt_name_base_files(path_list):
    alt_name_base_list = []
    for path in path_list:
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            alt_name_base_list.extend([AltNameBase._make(x) for x in reader])
    return alt_name_base_list


# CityExtra
CityExtra = namedtuple("CityExtra", "id latitude longitude elevation")

def read_city_extra_files(path_list):
    city_extra_list = []
    for path in path_list:
        with open(path, encoding="utf8") as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            city_extra_list.extend([CityExtra._make(x) for x in reader])
    return city_extra_list
