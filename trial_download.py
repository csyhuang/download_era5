#!/usr/bin/env python
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'pressure_level':[
            '1','2','3',
            '5','7','10',
            '20','30','50',
            '70','100','125',
            '150','175','200',
            '225','250','300',
            '350','400','450',
            '500','550','600',
            '650','700','750',
            '775','800','825',
            '850','875','900',
            '925','950','975',
            '1000'
        ],
        'variable':[
            'geopotential','temperature','u_component_of_wind',
            'v_component_of_wind','vertical_velocity'
        ],
        'time':[
            '00:00','06:00','12:00',
            '18:00'
        ],
        'product_type':'reanalysis',
        'year':'1979',
        'day':['01'],
        'month':'01',
        'format':'netcdf'
    },
    'download.nc')