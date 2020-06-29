# Download ERA5 data

## Create environment to run the scripts

For the first time you run the script:
```bash
conda create -n dlera5 python=3.7 lxml pandas
conda activate dlera5
pip install cdsapi
```

In the future, you only need to activate the environment before running the script by
```bash
conda activate dlera5
```
Define your download task in `task_definition.yaml`(see below).

In this directory(which contains `download_api.py`), run:
```bash
python download_api.py
```
The file will be downloaded to the local directory.

## Define a download task

The task is specified in `task_definition.yaml`. The data will be grouped monthly into netCDF files with the filename
`year_month_shortname.nc` and saved in the same directory as where the script `download_api.py` stands.

In `task_definition.yaml`, there are several parameters to set:
- `"start_year_month"`: it is a string that specifies the first month of data you want, e.g. Jan 2019 would be `201901`.
- `"end_year_month"`: it is a string that specifies the last month of data you want, e.g. Jun 2020 would be `202006`.
- `"grid_resolution"`: grid resolution of the netCDF file.
- `"times_in_a_day"`: time points in a day (the spacing of the time points would be the temporal resolution)
- `"reanalysis-era5-pressure-levels"`: an array of string of pressure-level variable names (Variable name in CDS). 
See [Table 9](https://confluence.ecmwf.int/pages/viewpage.action?pageId=82870405#ERA5:datadocumentation-Table9) on the 
ERA5 data documentation page for available variables to download.
- `"reanalysis-era5-single-levels"`: an array of string of single-level variable names (Variable name in CDS). 
See Table 1-6 and 8 on the 
[ERA5 data documentation page](https://confluence.ecmwf.int/pages/viewpage.action?pageId=82870405) for available 
variables to download.

## In the current `task_definition.yaml` file
- Date range: Dec 2019 - Jan 2020
- Spatial Resolution: 1 degree x 1 degree, 6 hourly data
- Time resolution: Every 6 hours
- Pressure level analysis variables:  
    - geopotential
    - temperature
    - u
    - v
    - vertical velocity
- Surface/single level variables:
    - land-sea mask
    - surface pressure
    - sea surface temperature
    - instantaneous surface sensible heat flux
    - large-scale precipitation
    - convective precipitation
