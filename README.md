# Download ERA5 data to Winds

## Python environment to run the scripts
```bash
pip install cdsapi
conda install -c anaconda lxml
conda install -c anaconda pandas
```

## Data to be downloaded
Type: pressure level analysis  
Resolution:, 1 degree x 1 degree, 6 hourly data  
Variables:  
- geopotential
- temperature
- u
- v
- vertical velocity

Type: surface (2D) variables  
Resolution:, 1 degree x 1 degree, 6 hourly data  
Variables:  s
- land-sea mask
- surface pressure
- sea surface temperature
- sensible heat flux
- large-scale precipitation
- convective precipitation
