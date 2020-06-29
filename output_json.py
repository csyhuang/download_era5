import json
from pprint import pprint
from datetime import date, timedelta
from pprint import pprint
import pandas as pd

sample_dictionary = {
    "start_year_month": "201803",
    "end_year_month": "202003",
    "grid_resolution": "1.0/1.0",
    "times_in_a_day": ["00:00", "06:00", "12:00", "18:00"],
    "reanalysis-era5-pressure-levels": [
        "geopotential",
        "temperature",
        "u_component_of_wind",
        "v_component_of_wind",
        "vertical_velocity",
    ],
    "reanalysis-era5-single-levels": [
        "instantaneous_surface_sensible_heat_flux",
        "land_sea_mask",
        "sea_surface_temperature",
        "surface_pressure",
    ],
}

with open("config.yaml") as f:
    text = f.read()
    dd = json.loads(text)
    # pprint(dd)


class YearMonth(object):
    def __init__(self, year, month):
        self._year = year
        if month not in range(1, 13):
            raise ValueError("month must be within the range between 1 and 12.")
        self._month = month

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    def next_month(self):
        if self._month + 1 == 13:
            self._year += 1
            self._month = 1
        else:
            self._month += 1

    def check_equal(self, year_month_object):
        if self.year == year_month_object.year and self.month == year_month_object.month:
            return True
        return False


if __name__ == "__main__":
    # start_year_month = YearMonth(2011, 3)
    # end_year_month = YearMonth(2012, 5)
    # while not start_year_month.check_equal(end_year_month):
    #     start_year_month.next_month()
    #     print(start_year_month.year, start_year_month.month)

    # ['count', 'name', 'units', 'Variable name in CDS', 'shortName', 'paramId', 'an', 'fc']
    # df = pd.read_csv("Table_9.csv", delimiter="|")
    df = pd.concat([pd.read_csv(f"Table_{i}.csv", delimiter="|") for i in range(1, 7)])

    valid_dict = {}
    for index, row in df.iterrows():
        valid_dict[row['Variable name in CDS']] = row['shortName']
    pprint(valid_dict)
    print(df.columns)
    print(df.head())
