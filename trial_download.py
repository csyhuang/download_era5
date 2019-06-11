#!/usr/bin/env python
import cdsapi
 
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete', {
    'class'   : 'ea',
    'expver'  : '1',
    'stream'  : 'oper',
    'type'    : 'fc',
    'step'    : '3/to/12/by/3',
    'param'   : '130.128',
    'levtype' : 'ml',
    'levelist': '1/10/50/100',
    'date'    : '2013-01-01',
    'time'    : '06/18',
    'area'    : '80/-50/-25/0', # North, West, South, East. Default: global
    'grid'    : '1.0/1.0', # Latitude/longitude grid: east-west (longitude) and north-south resolution (latitude). Default: reduced Gaussian grid
    'format'  : 'netcdf', # Default: grib
}, 'temp-fc-ml.nc')