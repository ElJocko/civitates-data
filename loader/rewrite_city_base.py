import csv
from collections import namedtuple
import civitates_data


# CityBase
OldCityBase = namedtuple("CityBase", "id geonames_name geonames_cc prefix")
NewCityBase = namedtuple("NewCityBase", "id geonames_name geonames_cc prefix wikipedia_article_name")


old_base_path = "../data"
new_base_path = "../new_data"
def rewrite_city_base():
    # Read CityBase files
    old_path_list = civitates_data.make_path_list_from_folders(old_base_path, "CityBase.txt")
    new_path_list = civitates_data.make_path_list_from_folders(new_base_path, "CityBase.txt")

    for i in range(len(old_path_list)):
        old_path = old_path_list[i]
        print(old_path)
        with open(old_path, encoding="utf8") as read_file:
            reader = csv.reader(read_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            city_list = []
            city_list.extend([OldCityBase._make(x) for x in reader])

        new_path = new_path_list[i]
        print(new_path)
        with open(new_path, 'w', encoding='utf8', newline='') as write_file:
            writer = csv.writer(write_file, delimiter='\t', quoting=csv.QUOTE_NONE)
            for city in city_list:
                city_dict = city._asdict()
                city_dict["wikipedia_article_name"] = city_dict["id"]
                new_city = NewCityBase(**city_dict)
                writer.writerow(new_city)


if __name__ == "__main__":
    rewrite_city_base()