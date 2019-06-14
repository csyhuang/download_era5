#!/usr/bin/env python
import cdsapi
from parallel import parallel_process
from calendar import monthrange

# === Years of data to download ===
start_year = 1982
end_year = 2019

# === Define download task ===
short_names = {
    'geopotential':  'z',
    'temperature':  't',
    'u_component_of_wind':  'u',
    'v_component_of_wind':  'v',
    'vertical_velocity':  'w'
}
n_processors = len(list(short_names))

# === Create connection client ===
cdsapi_client = cdsapi.Client()


# === Define task ===
def download_era5_data(year, month, variable_name, client):

    filename = \
        '{}_{:02d}_{}.nc'.format(year, month, short_names[variable_name])

    print('Start downloading {}'.format(filename))

    # Get number of days in a month
    weekday, num_of_days = monthrange(year, month)

    print('year = {}; month = {}'.format(year, month))

    client.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'pressure_level': [
                '1', '2', '3',
                '5', '7', '10',
                '20', '30', '50',
                '70', '100', '125',
                '150', '175', '200',
                '225', '250', '300',
                '350', '400', '450',
                '500', '550', '600',
                '650', '700', '750',
                '775', '800', '825',
                '850', '875', '900',
                '925', '950', '975',
                '1000'
            ],
            'variable': [variable_name],
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'grid': '1.0/1.0',
            'product_type': 'reanalysis',
            'year': '{}'.format(year),
            'day': ['{:02d}'.format(day) for day in range(1, num_of_days + 1)],
            'month': '{:02d}'.format(month),
            'format': 'netcdf'
        },
        filename
    )
    print('Finished downloading {}'.format(filename))
    return filename


def loop_over_months_and_years(variable_name, start_year, end_year, client):

    for year in range(start_year, end_year+1):
        for month in range(1, 12+1):
            fname = download_era5_data(year, month, variable_name, client)

    return 'Finished downloading {}'.format(variable_name)


if __name__ == "__main__":

    parallel_process(
        array=list(short_names),
        function=loop_over_months_and_years,
        n_jobs=n_processors,
        use_kwargs=False,
        extra_kwargs={
            'start_year': start_year,
            'end_year': end_year,
            'client': cdsapi_client
        }
    )

    print('End job: start_year = 1979; end_year = 1981.')


