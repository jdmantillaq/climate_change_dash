# %%
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
import warnings
warnings.filterwarnings("ignore")

sns.set(style="whitegrid")
sns.set_context('notebook', font_scale=1.3)


def get_files_in_folder(path, pattern):
    return np.sort(glob.glob(os.path.join(path, pattern)))

# %%
root = '/home/cambio_climatico/climate_index_data/ERA5/Indices/'

index_ls = ['TXx', 'TXn', 'TNx', 'TNn', 'TX90p', 'TX10p', 'TN90p',
            'TN10p', 'DTR', 'WSDI']

index_ls = ['TN90p', 'TN10p']
# index_ls = ['TX10p']

time_range = '1979-2014'
ds_dic = {}
source = 'ERA5'
scenario = 'historical'

lon_min = -115+360
lon_max = -30+360
lat_min = -10
lat_max = 30
img_extent = (lon_min,  lat_min, lon_max, lat_max)


# %%

for index_i in index_ls:
    print(index_i)
    path_i = get_files_in_folder(root, f'{index_i}*{time_range}.nc')[0]
    ds_i = xr.open_dataset(path_i)
    ds_dic[index_i] = ds_i.sel(lon=slice(lon_min, lon_max),
                               lat=slice(lat_max, lat_min))
    
# %%
proj_2 = ccrs.PlateCarree(central_longitude=0)
proj = ccrs.epsg(3857)


path_fig = '/home/cambio_climatico/climate_change_dash/assets/'

for i, index in enumerate(index_ls):
    # print(index,date.strftime('%d%m'))
    fig = plt.figure(figsize=(15, 7), facecolor='w', edgecolor='w')
    ax = plt.subplot(1, 1, 1, projection=proj)
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])

    cmap = index_prop[index]['cmap']
    levels = index_prop[index]['var_values']

    ds = ds_dic[index][index].median(dim='time')
    lat_values = ds.lat.values
    lon_values = ds.lon.values
    var_values = ds.values
    trend = ds_dic[index]['trend'].values
    significance = ds_dic[index]['significance'].values
    
    # data_contour = ax.contourf(lon_values, lat_values, var_values,
    #                            cmap=cmap,
    #                            #vmin=levels[0], vmax=levels[-1],
    #                            levels=np.linspace(levels[0],
    #                                               levels[-1], 21),
    #                            extend='both', zorder=0)
    
    # ax.coastlines(resolution=f'10m', color='k',
    #               lw=2, zorder=90)
    # ax.set_extent(img_extent, proj_2)

    ax.pcolormesh(lon_values, lat_values, var_values,
                  cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                  transform=proj)
    namefig = f'{source}_{index}_{scenario}_{time_range}'
    plt.savefig(f"{path_fig}{namefig}.png", pad_inches=0.0,
                bbox_inches='tight', dpi=500, transparent=True)
    

    plt.close(fig)
    
    fig = plt.figure(figsize=(15, 7), facecolor='w', edgecolor='w')
    ax = plt.subplot(1, 1, 1, projection=proj)
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])
    
    cmap = index_prop[index]['cmap_trend']
    levels = index_prop[index]['trend_values']
    
    ax.pcolormesh(lon_values, lat_values, trend,
                  cmap=cmap, vmin=levels.min(),
                  vmax=levels.max(),
                  transform=proj)
    namefig = f'{source}_{index}_trend_{scenario}_{time_range}'
    plt.savefig(f"{path_fig}{namefig}.png", pad_inches=0.0,
                bbox_inches='tight', dpi=500, transparent=True)
    plt.close(fig)

# %%

