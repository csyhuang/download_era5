"""
API to download netCDF based on task_definition.yaml
"""
import json
from datetime import date, datetime
from calendar import monthrange
import cdsapi


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


# Create a class to do all these
class DownloadERA5(object):
    def __init__(self, config="task_definition.yaml"):
        self._cdsapi_client = cdsapi.Client()
        self._all_pressure_level = [
            '1', '2', '3', '5', '7', '10', '20', '30', '50', '70', '100', '125', '150', '175', '200',
            '225', '250', '300', '350', '400', '450', '500', '550', '600', '650', '700', '750', '775',
            '800', '825', '850', '875', '900', '925', '950', '975', '1000']
        with open(config) as f:
            self._config_dict = json.loads(f.read())
        self._start_date = datetime.strptime(self._config_dict['start_year_month'], '%Y%m').date()
        self._end_date = datetime.strptime(self._config_dict['end_year_month'], '%Y%m').date()
        self._grid_resolution = self._config_dict['grid_resolution']
        self._time_in_a_day = self._config_dict['time_in_a_day']
        with open("variable_tables/pressure_level_params.json") as fp:
            self._valid_presure_level_params = json.load(fp)
        with open("variable_tables/single_level_params.json") as fp:
            self._valid_single_level_params = json.load(fp)

        for item in self._config_dict['reanalysis-era5-pressure-levels']:
            if item not in self.valid_presure_level_params:
                raise ValueError(f"{item} is not a valid pressure level variables to download.")
        self._pressure_levels_var = self._config_dict['reanalysis-era5-pressure-levels']

        for item in self._config_dict['reanalysis-era5-single-levels']:
            if item not in self.valid_single_level_params:
                raise ValueError(f"{item} is not a valid single level variables to download.")
        self._single_level_var = self._config_dict['reanalysis-era5-single-levels']

    @staticmethod
    def get_year_month_pairs(start_year, start_month, end_year, end_month):
        year_month_pairs = [(start_year, start_month)]
        initial_pair = YearMonth(start_year, start_month)
        while not initial_pair.check_equal(YearMonth(end_year, end_month)):
            initial_pair.next_month()
            year_month_pairs.append((initial_pair.year, initial_pair.month))
        year_month_pairs.append((end_year, end_month))
        return year_month_pairs

    def download_era5_pressure_level_data(self, year, month, dates, variable_name, filename):
        self._cdsapi_client.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'pressure_level': self._all_pressure_level,
                'variable': [variable_name],
                'time': self._time_in_a_day,
                'grid': self._grid_resolution,
                'product_type': 'reanalysis',
                'year': '{}'.format(year),
                'day': dates,
                'month': '{:02d}'.format(month),
                'format': 'netcdf'
            },
            filename
        )

    def download_single_level_data(self, year, month, dates, variable_name, filename):
        self._cdsapi_client.retrieve(
            'reanalysis-era5-single-levels',
            {
                'variable': [variable_name],
                'time': self._time_in_a_day,
                'grid': self._grid_resolution,
                'product_type': 'reanalysis',
                'year': '{}'.format(year),
                'day': dates,
                'month': '{:02d}'.format(month),
                'format': 'netcdf'
            },
            filename
        )

    @property
    def valid_presure_level_params(self):
        return self._valid_presure_level_params

    @property
    def valid_single_level_params(self):
        return self._valid_single_level_params

    def run(self, test_run=False):
        year_month_pairs = self.get_year_month_pairs(
            start_year=self._start_date.year,
            start_month=self._start_date.month,
            end_year=self._end_date.year,
            end_month=self._end_date.month,
        )
        for year, month in year_month_pairs:
            weekday, num_of_days = monthrange(year, month)
            date_list = ['1'] if test_run else ['{:02d}'.format(day) for day in range(1, num_of_days + 1)]
            if len(self._pressure_levels_var) > 0:
                for variable_name in self._pressure_levels_var:
                    short_name = self.valid_presure_level_params.get(variable_name)
                    filename = '{}_{:02d}_{}.nc'.format(year, month, short_name)
                    self.download_era5_pressure_level_data(
                        year, month, date_list, variable_name, filename)
                    print(f"Finished downloading {filename}")
            if len(self._single_level_var) > 0:
                for variable_name in self._single_level_var:
                    short_name = self.valid_single_level_params.get(variable_name)
                    filename = '{}_{:02d}_{}.nc'.format(year, month, short_name)
                    self.download_single_level_data(
                        year, month, date_list, variable_name, filename)
                    print(f"Finished downloading {filename}")


if __name__ == "__main__":
    download_era5 = DownloadERA5()
    download_era5.run()
