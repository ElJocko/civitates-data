from collections import namedtuple
import csv

PleiadesPlace = namedtuple("PleiadesPlace", "authors bbox connects_with created creators current_version description extent feature_types geo_context has_connections_with id location_precision max_date min_date modified path repr_lat repr_lat_long repr_long tags time_periods time_periods_keys time_periods_range title uid")

def read_pleiades_place_file(path):
    with open(path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # skip the header row
        pleiades_place_list = [PleiadesPlace._make(x) for x in reader]
        return pleiades_place_list
