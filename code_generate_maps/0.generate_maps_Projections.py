# %%



import warnings
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import glob
import os
import sys
sys.path.append('/home/cambio_climatico/climate_change_dash/')
from properties import index_prop

# To ignore warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
sns.set_context('notebook', font_scale=1.3)


def get_files_in_folder(path, pattern):
    return np.sort(glob.glob(os.path.join(path, pattern)))



path_fig = '/home/cambio_climatico/climate_change_dash/assets/'


def plots_index(lon_values, lat_values, var_values, cmap=None, levels=None):
    proj = ccrs.epsg(3857)

    fig = plt.figure(figsize=(15, 7), facecolor='w', edgecolor='w')
    ax = plt.subplot(1, 1, 1, projection=proj)
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])

    ax.pcolormesh(lon_values, lat_values, var_values,
                  cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                  transform=proj)
    return fig


# Define the project dictionary with climate models, scenarios, and variables
project = {
    'NEX-GDDP-CMIP6': {'models':
                       {'pr': ['BCC-CSM2-MR', 'MIROC6', 'MPI-ESM1-2-LR',
                               'MRI-ESM2-0', 'NorESM2-LM'],
                        'tas': ['BCC-CSM2-MR', 'MIROC6', 'MPI-ESM1-2-LR',
                                'MRI-ESM2-0', 'NorESM2-LM'],
                        # 'pr': ['BCC-CSM2-MR', 'MIROC6', 'MRI-ESM2-0'],
                        # 'tas': ['MIROC6', 'MPI-ESM1-2-LR', 'NorESM2-LM']
                        },
                       'scenarios': {'historical': 'historical',
                                     'ssp585': 'ssp585',
                                     'ssp245': 'ssp245'}},

    'HighResMIP-CMIP6': {'models':
                         {'pr': ['MRI-AGCM3-2-S'],
                          'tas': ['MRI-AGCM3-2-S']},
                         'scenarios': {'historical': 'highresSST-present',
                                       'ssp585': 'highresSST-future'}}}

# Define a dictionary to map scenario keys to their labels
label_ssp = {'ssp245': 'SSP2-4.5',
             'ssp585': 'SSP5-8.5',
             'highresSST-future': 'RCP 8.5: highresSST-future'}

# Define a dictionary for time ranges for
# precipitation (pr) and temperature (tas)
time_range_dic = {'pr': [np.arange(1981, 2015),
                         np.arange(2021, 2041),
                         np.arange(2041, 2061),
                         np.arange(2061, 2081),
                         np.arange(2081, 2101)],
                  'tas': [np.arange(1979, 2015),
                          np.arange(2021, 2041),
                          np.arange(2041, 2061),
                          np.arange(2061, 2081),
                          np.arange(2081, 2101)]}


# Define a dictionary to map scenario keys to their labels
label_ssp = {'ssp245': 'SSP2-4.5',
             'ssp585': 'SSP5-8.5',
             # 'highresSST-future': 'RCP 8.5: highresSST-future',
             'highresSST-future': 'RCP8.5'}


# Define the analysis variable (pr in this case)
analisys = 'pr'

# Define the source models to be used
source = ['NEX-GDDP-CMIP6', 'HighResMIP-CMIP6']
source = ['HighResMIP-CMIP6']

# Define the scenario keys to be analyzed
scenarios_key = ['ssp585', 'ssp245']

# Define a list of lists containing climate indices
index_ls = ['PRCPTOT']

# index_ls = ['TXn']

# Define the path for climate index data
path = '/home/cambio_climatico/climate_index_data/'

# Get the time ranges for the selected analysis variable (pr or tas)
time_range = time_range_dic[analisys]

# Convert time ranges to strings for printing
time_range_str = [f'{i[0]}-{i[-1]}' for i in time_range]


lon_min = -115+360
lon_max = -30+360
lat_min = -10
lat_max = 30


for source_i in source:
    models = project[source_i]['models'][analisys]
    scenarios = project[source_i]['scenarios']
    for model_i in models:
        for sk_i in scenarios_key:
            print(f'{"/".join([source_i, model_i, sk_i])}')
            ds_dic = {}
            try:
                time_list = list(zip([scenarios['historical'],
                                      scenarios[sk_i],
                                      scenarios[sk_i],
                                      scenarios[sk_i],
                                      scenarios[sk_i]],
                                     time_range_str))
            except KeyError:
                continue
            # for ii, index_ls_i in enumerate(index_ls):
            for index_i in index_ls:
                print(f'\t{index_i}')
                ds_index = {}

                for ii, (s_i, t_i) in enumerate(time_list):

                    # leer los datos históricos
                    source_x = [source_i, model_i, s_i]

                    print(f'\t\t{s_i}: {t_i}')
                    root = f'{path}{"/".join(source_x)}/Indices/'

                    path_i = \
                        get_files_in_folder(root,
                                            f'{index_i}*{t_i}.nc')[0]
                    ds_i = xr.open_dataset(path_i)
                    ds_i = ds_i.sel(lon=slice(lon_min, lon_max),
                                    lat=slice(lat_min, lat_max))

                    if ii == 0:
                        ds_hist = ds_i
                    else:

                        cmap = index_prop[index_i]['cmap']
                        levels = index_prop[index_i]['var_values_proj']

                        lat_values = ds_i.lat.values
                        lon_values = ds_i.lon.values
                        var_values = ds_i[index_i].median(dim='time').values

                        fig = plots_index(lon_values,
                                          lat_values,
                                          var_values,
                                          cmap=cmap,
                                          levels=levels)

                        namefig = f'{model_i}_{index_i}_{label_ssp[s_i]}_{t_i}'
                        fig.savefig(f"{path_fig}{namefig}.png", pad_inches=0.0,
                                    bbox_inches='tight', dpi=500,
                                    transparent=True)

                        var_values = ds_i[index_i].median(dim='time').values -\
                            ds_hist[index_i].median(dim='time').values
                        cmap = index_prop[index_i]['cmap_anom_proj']
                        levels = index_prop[index_i]['anom_values_proj']
                        fig = plots_index(lon_values,
                                          lat_values,
                                          var_values,
                                          cmap=cmap,
                                          levels=levels)

                        namefig = f'{model_i}_{index_i}_anom_{label_ssp[s_i]}_{t_i}'
                        fig.savefig(f"{path_fig}{namefig}.png", pad_inches=0.0,
                                    bbox_inches='tight', dpi=500,
                                    transparent=True)
                        
                        plt.close('all')

#%%