This project holds the city data for the Civitates apps.

In order to make it easier to manage, the data is divided by region.
The files for each region are stored in that region's folder, e.g., `data/Italy`.
Note that the regions are only used to represent broad geographical areas and are not intended to make any statement or express any belief about past or current political or ethnic boundaries.

### Files

Files contain data in CSV format, encoded in UTF-8 characters. Each region has four files:

* `CityBase.txt` contains one row for each city and provides core information for the cities.
* `AltNameBase.txt` contains one row for each name that applies to a city.
* `PeriodBase.txt` contains one row for each time period identified for a city. This is the primary information used to determine which cities to display at a particular date and zoom level.
* `CityExtra.txt` contains additional information for a city location when necessary. The location for most cities is extracted from the `cities1000.txt` or `pleiades-places.csv` files, but any city that doesn't have location data available in those files will have one row in this file.

#### CityBase.txt

`CityBase.txt` has the following columns:

* `id`  Name of the city. Used as an identifier across the files in its region. Must be unique within the region, but not across regions.
* `geonames_name`  Value used to look up the city in `cities1000.txt` or `pleiades-places.csv`.
* `geonames_cc`  "P" indicates the city location should be found in `pleiades-places.csv`. "X" indicates the city location should be found in `CityExtra.txt`. Any two letter value is used in locating the city in `cities1000.txt`.
* `prefix`  Prefix to use when displaying the primary city name.
* `wikipedia_article_name`  Value to use when retrieving the Wikipedia article for this city.

#### AltNameBase.txt

`AltNameBase.txt` has the following columns:

* `id`  Identifier for the city. Must match the `id` in `CityBase.txt`.
* `alt_name`  A name used for the city.
* `language`  Primary language or culture associated with this name.

#### PeriodBase.txt

`PeriodBase.txt` has the following columns:

* `id`  Identifier for the city. Must match the `id` in `CityBase.txt`.
* `start_date`  Start date for the time period. Negative values represent BC.
* `end_date`  End date for the time period. Negative values represent BC.
* `preferredName`  Name to display for the city during this period.
* `size`  Size or prominence of the city during this period. Ranges between 0 (largest and most prominent) to 4 (smallest and least prominent)
* `tag_position` Where to display the city name on the map, relative to the city graphic. Ranges between 0 and 7.

```
2  4  0
6  .  5
3  7  1
```

Note that time periods for a city must not overlap.

#### CityExtra.txt

`CityExtra.txt` has the following columns:

* `id`  Identifier for the city. Must match the `id` in `CityBase.txt`.
* `latitude`  Decimal latitude for the city.
* `longitude`  Decimal longitude for the city.
* `elevation`  Elevation of the city in meters. A value of 0 is used when the elevation hasn't been determined.

