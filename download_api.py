"""
API to download netCDF based on config.yaml
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
    def __init__(self, config="config.yaml"):
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

    def download_era5_pressure_level_data(self, year, month, num_of_days, variable_name, filename):
        self._cdsapi_client.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'pressure_level': self._all_pressure_level,
                'variable': [variable_name],
                'time': self._time_in_a_day,
                'grid': self._grid_resolution,
                'product_type': 'reanalysis',
                'year': '{}'.format(year),
                'day': ['1'],
                # 'day': ['{:02d}'.format(day) for day in range(1, num_of_days + 1)],
                'month': '{:02d}'.format(month),
                'format': 'netcdf'
            },
            filename
        )

    def download_single_level_data(self, year, month, num_of_days, variable_name, filename):
        self._cdsapi_client.retrieve(
            'reanalysis-era5-single-levels',
            {
                'variable': [variable_name],
                'time': self._time_in_a_day,
                'grid': self._grid_resolution,
                'product_type': 'reanalysis',
                'year': '{}'.format(year),
                'day': ['1'],
                # 'day': ['{:02d}'.format(day) for day in range(1, num_of_days + 1)],
                'month': '{:02d}'.format(month),
                'format': 'netcdf'
            },
            filename
        )

    @property
    def valid_presure_level_params(self):
        return {
            'divergence': 'd',
            'fraction_of_cloud_cover': 'cc',
            'geopotential': 'z',
            'ozone_mass_mixing_ratio': 'o3',
            'potential_vorticity': 'pv',
            'relative_humidity': 'r',
            'specific_cloud_ice_water_content': 'ciwc',
            'specific_cloud_liquid_water_content': 'clwc',
            'specific_humidity': 'q',
            'specific_rain_water_content': 'crwc',
            'specific_snow_water_content': 'cswc',
            'temperature': 't',
            'u_component_of_wind': 'u',
            'v_component_of_wind': 'v',
            'vertical_velocity': 'w',
            'vorticity': 'vo'}

    @property
    def valid_single_level_params(self):
        return {
            '100m_u_component_of_wind': '100u',
            '100m_v_component_of_wind': '100v',
            '10m_u_component_of_neutral_wind': 'u10n',
            '10m_u_component_of_wind': '10u',
            '10m_v_component_of_neutral_wind': 'v10n',
            '10m_v_component_of_wind': '10v',
            '10m_wind_gust_since_previous_post_processing': '10fg',
            '2m_dewpoint_temperature': '2d',
            '2m_temperature': '2t',
            'angle_of_sub_gridscale_orography': 'anor',
            'anisotropy_of_sub_gridscale_orography': 'isor',
            'boundary_layer_dissipation': 'bld',
            'boundary_layer_height': 'blh',
            'charnock': 'chnk',
            'clear_sky_direct_solar_radiation_at_surface': 'cdir',
            'cloud_base_height': 'cbh',
            'convective_available_potential_energy': 'cape',
            'convective_inhibition': 'cin',
            'convective_precipitation': 'cp',
            'convective_rain_rate': 'crr',
            'convective_snowfall': 'csf',
            'convective_snowfall_rate_water_equivalent': 'csfr',
            'downward_uv_radiation_at_the_surface': 'uvb',
            'duct_base_height': 'dctb',
            'eastward_gravity_wave_surface_stress': 'lgws',
            'eastward_turbulent_surface_stress': 'ewss',
            'evaporation': 'e',
            'forecast_albedo': 'fal',
            'forecast_logarithm_of_surface_roughness_for_heat': 'flsr',
            'forecast_surface_roughness': 'fsr',
            'friction_velocity': 'zust',
            'geopotential': 'z',
            'gravity_wave_dissipation': 'gwd',
            'high_cloud_cover': 'hcc',
            'high_vegetation_cover': 'cvh',
            'ice_temperature_layer_1': 'istl1',
            'ice_temperature_layer_2': 'istl2',
            'ice_temperature_layer_3': 'istl3',
            'ice_temperature_layer_4': 'istl4',
            'instantaneous_10m_wind_gust': 'i10fg',
            'instantaneous_eastward_turbulent_surface_stress': 'iews',
            'instantaneous_large_scale_surface_precipitation_fraction': 'ilspf',
            'instantaneous_moisture_flux': 'ie',
            'instantaneous_northward_turbulent_surface_stress': 'inss',
            'instantaneous_surface_sensible_heat_flux': 'ishf',
            'k_index': 'kx',
            'lake_bottom_temperature': 'lblt',
            'lake_cover': 'cl',
            'lake_depth': 'dl',
            'lake_ice_depth': 'licd',
            'lake_ice_temperature': 'lict',
            'lake_mix_layer_depth': 'lmld',
            'lake_mix_layer_temperature': 'lmlt',
            'lake_shape_factor': 'lshf',
            'lake_total_layer_temperature': 'ltlt',
            'land_sea_mask': 'lsm',
            'large_scale_precipitation': 'lsp',
            'large_scale_precipitation_fraction': 'lspf',
            'large_scale_rain_rate': 'lsrr',
            'large_scale_snowfall': 'lsf',
            'large_scale_snowfall_rate_water_equivalent': 'lssfr',
            'leaf_area_index_high_vegetation': 'lai_hv',
            'leaf_area_index_low_vegetation': 'lai_lv',
            'low_cloud_cover': 'lcc',
            'low_vegetation_cover': 'cvl',
            'maximum_2m_temperature_since_previous_post_processing': 'mx2t',
            'maximum_total_precipitation_rate_since_previous_post_processing': 'mxtpr',
            'mean_boundary_layer_dissipation': 'mbld',
            'mean_convective_precipitation_rate': 'mcpr',
            'mean_convective_snowfall_rate': 'mcsr',
            'mean_eastward_gravity_wave_surface_stress': 'megwss',
            'mean_eastward_turbulent_surface_stress': 'metss',
            'mean_evaporation_rate': 'mer',
            'mean_gravity_wave_dissipation': 'mgwd',
            'mean_large_scale_precipitation_fraction': 'mlspf',
            'mean_large_scale_precipitation_rate': 'mlspr',
            'mean_large_scale_snowfall_rate': 'mlssr',
            'mean_northward_gravity_wave_surface_stress': 'mngwss',
            'mean_northward_turbulent_surface_stress': 'mntss',
            'mean_potential_evaporation_rate': 'mper',
            'mean_runoff_rate': 'mror',
            'mean_sea_level_pressure': 'msl',
            'mean_snow_evaporation_rate': 'mser',
            'mean_snowfall_rate': 'msr',
            'mean_snowmelt_rate': 'msmr',
            'mean_sub_surface_runoff_rate': 'mssror',
            'mean_surface_direct_short_wave_radiation_flux': 'msdrswrf',
            'mean_surface_direct_short_wave_radiation_flux_clear_sky': 'msdrswrfcs',
            'mean_surface_downward_long_wave_radiation_flux': 'msdwlwrf',
            'mean_surface_downward_long_wave_radiation_flux_clear_sky': 'msdwlwrfcs',
            'mean_surface_downward_short_wave_radiation_flux': 'msdwswrf',
            'mean_surface_downward_short_wave_radiation_flux_clear_sky': 'msdwswrfcs',
            'mean_surface_downward_uv_radiation_flux': 'msdwuvrf',
            'mean_surface_latent_heat_flux': 'mslhf',
            'mean_surface_net_long_wave_radiation_flux': 'msnlwrf',
            'mean_surface_net_long_wave_radiation_flux_clear_sky': 'msnlwrfcs',
            'mean_surface_net_short_wave_radiation_flux': 'msnswrf',
            'mean_surface_net_short_wave_radiation_flux_clear_sky': 'msnswrfcs',
            'mean_surface_runoff_rate': 'msror',
            'mean_surface_sensible_heat_flux': 'msshf',
            'mean_top_downward_short_wave_radiation_flux': 'mtdwswrf',
            'mean_top_net_long_wave_radiation_flux': 'mtnlwrf',
            'mean_top_net_long_wave_radiation_flux_clear_sky': 'mtnlwrfcs',
            'mean_top_net_short_wave_radiation_flux': 'mtnswrf',
            'mean_top_net_short_wave_radiation_flux_clear_sky': 'mtnswrfcs',
            'mean_total_precipitation_rate': 'mtpr',
            'mean_vertical_gradient_of_refractivity_inside_trapping_layer': 'dndza',
            'mean_vertically_integrated_moisture_divergence': 'mvimd',
            'medium_cloud_cover': 'mcc',
            'minimum_2m_temperature_since_previous_post_processing': 'mn2t',
            'minimum_total_precipitation_rate_since_previous_post_processing': 'mntpr',
            'minimum_vertical_gradient_of_refractivity_inside_trapping_layer': 'dndzn',
            'near_ir_albedo_for_diffuse_radiation': 'alnid',
            'near_ir_albedo_for_direct_radiation': 'alnip',
            'northward_gravity_wave_surface_stress': 'mgws',
            'northward_turbulent_surface_stress': 'nsss',
            'potential_evaporation': 'pev',
            'precipitation_type': 'ptype',
            'runoff': 'ro',
            'sea_ice_cover': 'ci',
            'sea_surface_temperature': 'sst',
            'skin_reservoir_content': 'src',
            'skin_temperature': 'skt',
            'slope_of_sub_gridscale_orography': 'slor',
            'snow_albedo': 'asn',
            'snow_density': 'rsn',
            'snow_depth': 'sd',
            'snow_evaporation': 'es',
            'snowfall': 'sf',
            'snowmelt': 'smlt',
            'soil_temperature_level_1': 'stl1',
            'soil_temperature_level_2': 'stl2',
            'soil_temperature_level_3': 'stl3',
            'soil_temperature_level_4': 'stl4',
            'soil_type': 'slt',
            'standard_deviation_of_filtered_subgrid_orography': 'sdfor',
            'standard_deviation_of_orography': 'sdor',
            'sub_surface_runoff': 'ssro',
            'surface_latent_heat_flux': 'slhf',
            'surface_net_solar_radiation': 'ssr',
            'surface_net_solar_radiation_clear_sky': 'ssrc',
            'surface_net_thermal_radiation': 'str',
            'surface_net_thermal_radiation_clear_sky': 'strc',
            'surface_pressure': 'sp',
            'surface_runoff': 'sro',
            'surface_sensible_heat_flux': 'sshf',
            'surface_solar_radiation_downward_clear_sky': 'ssrdc',
            'surface_solar_radiation_downwards': 'ssrd',
            'surface_thermal_radiation_downward_clear_sky': 'strdc',
            'surface_thermal_radiation_downwards': 'strd',
            'temperature_of_snow_layer': 'tsn',
            'toa_incident_solar_radiation': 'tisr',
            'top_net_solar_radiation': 'tsr',
            'top_net_solar_radiation_clear_sky': 'tsrc',
            'top_net_thermal_radiation': 'ttr',
            'top_net_thermal_radiation_clear_sky': 'ttrc',
            'total_cloud_cover': 'tcc',
            'total_column_cloud_ice_water': 'tciw',
            'total_column_cloud_liquid_water': 'tclw',
            'total_column_ozone': 'tco3',
            'total_column_rain_water': 'tcrw',
            'total_column_snow_water': 'tcsw',
            'total_column_supercooled_liquid_water': 'tcslw',
            'total_column_water': 'tcw',
            'total_column_water_vapour': 'tcwv',
            'total_precipitation': 'tp',
            'total_sky_direct_solar_radiation_at_surface': 'fdir',
            'total_totals_index': 'totalx',
            'trapping_layer_base_height': 'tplb',
            'trapping_layer_top_height': 'tplt',
            'type_of_high_vegetation': 'tvh',
            'type_of_low_vegetation': 'tvl',
            'uv_visible_albedo_for_diffuse_radiation': 'aluvd',
            'uv_visible_albedo_for_direct_radiation': 'aluvp',
            'vertical_integral_of_divergence_of_cloud_frozen_water_flux': 'viiwd',
            'vertical_integral_of_divergence_of_cloud_liquid_water_flux': 'vilwd',
            'vertical_integral_of_divergence_of_geopotential_flux': 'vigd',
            'vertical_integral_of_divergence_of_kinetic_energy_flux': 'viked',
            'vertical_integral_of_divergence_of_mass_flux': 'vimad',
            'vertical_integral_of_divergence_of_moisture_flux': 'viwvd',
            'vertical_integral_of_divergence_of_ozone_flux': 'viozd',
            'vertical_integral_of_divergence_of_thermal_energy_flux': 'vithed',
            'vertical_integral_of_divergence_of_total_energy_flux': 'vitoed',
            'vertical_integral_of_eastward_cloud_frozen_water_flux': 'viiwe',
            'vertical_integral_of_eastward_cloud_liquid_water_flux': 'vilwe',
            'vertical_integral_of_eastward_geopotential_flux': 'vige',
            'vertical_integral_of_eastward_heat_flux': 'vithee',
            'vertical_integral_of_eastward_kinetic_energy_flux': 'vikee',
            'vertical_integral_of_eastward_mass_flux': 'vimae',
            'vertical_integral_of_eastward_ozone_flux': 'vioze',
            'vertical_integral_of_eastward_total_energy_flux': 'vitoee',
            'vertical_integral_of_eastward_water_vapour_flux': 'viwve',
            'vertical_integral_of_energy_conversion': 'viec',
            'vertical_integral_of_kinetic_energy': 'vike',
            'vertical_integral_of_mass_of_atmosphere': 'vima',
            'vertical_integral_of_mass_tendency': 'vimat',
            'vertical_integral_of_northward_cloud_frozen_water_flux': 'viiwn',
            'vertical_integral_of_northward_cloud_liquid_water_flux': 'vilwn',
            'vertical_integral_of_northward_geopotential_flux': 'vign',
            'vertical_integral_of_northward_heat_flux': 'vithen',
            'vertical_integral_of_northward_kinetic_energy_flux': 'viken',
            'vertical_integral_of_northward_mass_flux': 'viman',
            'vertical_integral_of_northward_ozone_flux': 'viozn',
            'vertical_integral_of_northward_total_energy_flux': 'vitoen',
            'vertical_integral_of_northward_water_vapour_flux': 'viwvn',
            'vertical_integral_of_potential_and_internal_energy': 'vipie',
            'vertical_integral_of_potential_internal_and_latent_energy': 'vipile',
            'vertical_integral_of_temperature': 'vit',
            'vertical_integral_of_thermal_energy': 'vithe',
            'vertical_integral_of_total_energy': 'vitoe',
            'vertically_integrated_moisture_divergence': 'vimd',
            'volumetric_soil_water_layer_1': 'swvl1',
            'volumetric_soil_water_layer_2': 'swvl2',
            'volumetric_soil_water_layer_3': 'swvl3',
            'volumetric_soil_water_layer_4': 'swvl4'}

    def run(self):
        year_month_pairs = self.get_year_month_pairs(
            start_year=self._start_date.year,
            start_month=self._start_date.month,
            end_year=self._end_date.year,
            end_month=self._end_date.month,
        )
        for year, month in year_month_pairs:
            weekday, num_of_days = monthrange(year, month)
            if len(self._pressure_levels_var) > 0:
                for variable_name in self._pressure_levels_var:
                    short_name = self.valid_presure_level_params.get(variable_name)
                    filename = '{}_{:02d}_{}.nc'.format(year, month, short_name)
                    self.download_era5_pressure_level_data(
                        year, month, num_of_days, variable_name, filename)
                    print(f"Finished downloading {filename}")
            if len(self._single_level_var) > 0:
                for variable_name in self._single_level_var:
                    short_name = self.valid_single_level_params.get(variable_name)
                    filename = '{}_{:02d}_{}.nc'.format(year, month, short_name)
                    self.download_single_level_data(
                        year, month, num_of_days, variable_name, filename)
                    print(f"Finished downloading {filename}")


if __name__ == "__main__":
    download_era5 = DownloadERA5()
    download_era5.run()
