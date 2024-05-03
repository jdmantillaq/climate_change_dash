# %%
import sys
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import glob
import os

# To ignore warnings
import warnings
warnings.filterwarnings("ignore")

sns.set(style="whitegrid")
sns.set_context('notebook', font_scale=1.3)


def get_files_in_folder(path, pattern):
    return np.sort(glob.glob(os.path.join(path, pattern)))


def get_custom_color_palette_hash(option='BuRd'):
    from matplotlib.colors import LinearSegmentedColormap
    colors = ['#7F0821', '#B1182C', '#C84741', '#DF765D', '#F3A47F', '#FAC7AF',
              '#FBE4D6', '#FFFFFF', '#DDECF3', '#BBDBEA', '#90C3DC', '#5BA3CB',
              '#3784BC', '#2064AB', '#0E417A']

    if option == 'RdBu':
        pass
    elif option == 'BuRd' or option == 'RdBu_r':
        colors = colors[::-1]
    else:
        raise ValueError("Invalid option")

    return LinearSegmentedColormap.from_list("", colors)


cmap = get_custom_color_palette_hash('RdBu_r')


index_prop = {
    'R5mm': {'var_values': np.linspace(0, 250),
             'anom_values': np.linspace(-30, 30),
             'cmap': 'viridis', 'units': 'días/año'},
    'R10mm': {'var_values': np.linspace(0, 200),
              'anom_values': np.linspace(-30, 30),
              'cmap': 'viridis', 'units':  'días/año'},
    'R20mm': {'var_values': np.linspace(0, 250),
              'anom_values': np.linspace(-30, 30),
              'cmap': 'viridis', 'units':  'días/año'},
    'R50mm': {'var_values': np.linspace(0, 250),
              'anom_values': np.linspace(-30, 30),
              'cmap': 'viridis', 'units': 'días/año'},
    'CDD': {'var_values': np.linspace(0, 60),
            'anom_values': np.linspace(-10, 10),
            'cmap': 'plasma', 'units': 'días/año'},
    'CWD': {'var_values': np.linspace(0, 60),
            'anom_values': np.linspace(-10, 10),
            'cmap': 'plasma', 'units': 'días/año'},

    'R95p': {'var_values': np.linspace(0, 1000),
             'anom_values': np.linspace(-350, 350),
             'cmap': "Spectral_r",
             'units': 'mm/año'},
    'R99p': {'var_values': np.linspace(0, 400),
             'anom_values': np.linspace(-250, 250),
             'cmap': "Spectral_r",
             'units': 'mm/año'},
    'PRCPTOT': {'var_values': np.linspace(0, 6000),
                'anom_values': np.linspace(-900, 900),
                'cmap': "Spectral_r",
                'units': 'mm/año'},

    'SDII': {'var_values': np.linspace(0, 30),
             'anom_values': np.linspace(-5, 5),
             'cmap': "Spectral_r",
             'units': 'mm/día'},

    'P75y': {'var_values': np.linspace(0, 60),
             'anom_values': np.linspace(-8, 8),
             'cmap': "Spectral_r",
             'units': 'mm/día'},
    'P90y': {'var_values': np.linspace(0, 60),
             'anom_values': np.linspace(-8, 8),
             'cmap': "Spectral_r",
             'units': 'mm/día'},
    'P95y': {'var_values': np.linspace(0, 60),
             'anom_values': np.linspace(-8, 8),
             'cmap': "Spectral_r",
             'units': 'mm/día'},

    'P75p': {'var_values': np.linspace(0, 30),
             'anom_values': np.linspace(-8, 8),
             'cmap': "Spectral_r",
             'units': 'días/año'},
    'P90p': {'var_values': np.linspace(0, 30),
             'anom_values': np.linspace(-8, 8),
             'cmap': "Spectral_r",
             'units': 'días/año'},
    'P95p': {'var_values': np.linspace(0, 30),
             'anom_values': np.linspace(-8, 8),
             'cmap': "Spectral_r",
             'units': 'días/año'},

    'TXx': {'var_values': np.linspace(18, 42),
            'anom_values': np.linspace(-6, 6),
            'cmap': 'Spectral_r',
            'units': '°C'},
    'TXn': {'var_values': np.linspace(18, 42),
            'anom_values': np.linspace(-6, 6),
            'cmap': 'Spectral_r',
            'units': '°C'},
    
    'TNn': {'var_values': np.linspace(6, 32),
            'anom_values': np.linspace(-6, 6),
            'cmap': 'Spectral_r',
            'units': '°C'},
    
    'TNx': {'var_values': np.linspace(6, 32),
            'anom_values': np.linspace(-6, 6),
            'cmap': 'Spectral_r',
            'units': '°C'},

    'TN10p': {'var_values': np.linspace(0, 15),
              'anom_values': np.linspace(-10, 10),
              'cmap': 'viridis',
              'units': '% días/año'},
    'TN90p': {'var_values': np.linspace(0, 15),
              'anom_values': np.linspace(-80, 80),
              'cmap': 'viridis',
              'units': '% días/año'},

    'TX10p': {'var_values': np.linspace(6, 15),
              'anom_values': np.linspace(-15, 15),
              'cmap': 'viridis',
              'units': '% días/año'},
    'TX90p': {'var_values': np.linspace(6, 15),
              'anom_values': np.linspace(-90, 90),
              'cmap': 'viridis',
              'units': '% días/año'},

    'DTR': {'var_values': np.linspace(6, 18),
            'anom_values': np.linspace(-1, 1),
            'cmap': 'Spectral_r',
            'units': '°C'},

    'WSDI': {'var_values': np.linspace(0, 30),
             'anom_values': np.linspace(-250, 250),
             'cmap': 'plasma',
             'units': 'días/año'},
}

# %%
root = '/home/cambio_climatico/climate_index_data/ERA5/Indices/'

index_ls = ['TXx', 'TXn', 'TNx', 'TNn',
            'TX90p', 'TX10p', 'TN90p', 'TN10p',
            'DTR', 'WSDI']
time_range = '1979-2014'
ds_dic = {}
source = 'ERA5'
scenario = 'historical'


# %%

for index_i in index_ls:
    print(index_i)
    path_i = get_files_in_folder(root, f'{index_i}*{time_range}.nc')[0]
    ds_dic[index_i] = xr.open_dataset(path_i)
# %%
proj_2 = ccrs.PlateCarree(central_longitude=0)
proj = ccrs.epsg(3857)
img_extent = (-115+360,  -10, -30+360, 30)

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

    # ax.text(-56.5, -9.85,
    #         f"GPM IMERG PRECIPITATION L3 V06 / MODIS - Collection 6 · Acumulado {date.strftime('%d-%m-%y')}",
    #         fontsize=8, color="gray")

    namefig = f'{source}_{index}_{scenario}_{time_range}'
    plt.savefig(f"{path_fig}{namefig}.png", pad_inches=0.0,
                bbox_inches='tight', dpi=500, transparent=True)


# %%

# Define the map projection (PlateCarree) and set the image extent
proj = ccrs.PlateCarree(central_longitude=0)
img_extent = (-110, -35, -8, 25)


# Create a figure with a specified size
# fig = plt.figure(figsize=(8.5, 8))
fig = plt.figure(figsize=(9, 12))

# Define the grid size (number of rows and columns)
num_rows = 5
num_columns = 2

# Define properties for the grid
horiz_spacing = 0.17
vert_spacing = 0.03

# Use the function to calculate properties of the grid
grid_prop = x_coords, y_coords, x_fig, y_fig = cgp.define_grid_fig(
    num_rows, num_columns,
    horiz_spacing=horiz_spacing, vert_spacing=vert_spacing)

font_prop = {'fontsize': 15, 'fontweight': 'semibold', 'color': '#434343'}

h_space_intercol = 0.03
x_coords[-1] += h_space_intercol

x_cbar_0 = x_coords[0] + x_fig + 0.02
x_cbar_1 = x_coords[-1] + x_fig + 0.02
width_cbar = 0.015
y_cbar = y_fig*2 + vert_spacing

prop_grid = {'lat_step': 10, 'lon_step': 25}

scatter_prop = {'s': 12, 'edgecolors': 'k', 'lw': 0.1, 'c': 'k', 'marker': '.',
                'facecolor': None, 'alpha': 0.8, 'zorder': 40}

letras = np.array([chr(i) for i in range(65,
                                         65 + num_columns*num_rows)]
                  ).reshape((num_columns, num_rows))

fig.suptitle(f'{source}\n{scenario.title()} [{time_range}]',
             x=x_coords[0], y=1.01, fontsize=18,
             fontweight='bold', ha='left', va='bottom', color='#434343')

# -----------------------------------------------------------------------------
# Fila: 0 y 1, Columna 0. 'TXx' - 'TXn'
# -----------------------------------------------------------------------------

indieces = ['TXx', 'TXn']
levels = np.linspace(18, 42, 13)
label = '°C'
cmap = sns.color_palette("Spectral_r", as_cmap=True)
x_cbar = x_cbar_0
for i, ri in enumerate([0, 1]):
    for ci in [0]:
        # Add axes to the figure with the calculated properties
        ax = fig.add_axes([x_coords[ci], y_coords[ri],
                           x_fig, y_fig],
                          projection=proj)
        # Add geographic features to the plot
        ax = cgp.continentes_lon_lat(ax, **prop_grid)
        # Set the image extent and aspect ratio of the plot
        ax.set_extent(img_extent, proj)
        ax.set_aspect('auto')
        ax.set_title(f'{letras[ci][ri]}. {indieces[i]}', loc='left',
                     fontdict=font_prop)
        # Remove x-axis labels for subplots that are not in the last row
        if ri < (num_rows - 1):
            ax.set_xticklabels([])

        ds = ds_dic[indieces[ri]].median(dim='time')
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        var_values = ds[indieces[ri]].values

        cs = ax.pcolormesh(lon_values, lat_values, var_values,
                           cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                           transform=proj)

        ax.grid(False)

cbaxes = fig.add_axes([x_cbar, y_coords[ri], width_cbar, y_cbar])
fig.colorbar(cs, cax=cbaxes, orientation='vertical',
             label=label)

# -----------------------------------------------------------------------------
# Fila: 0 y 1, Columna 1. 'TNx' - 'TNn'
# -----------------------------------------------------------------------------

indieces = ['TNx', 'TNn']
levels = np.linspace(6, 32, 14)
label = '°C'
cmap = sns.color_palette("Spectral_r", as_cmap=True)
x_cbar = x_cbar_1
for i, ri in enumerate([0, 1]):
    for ci in [1]:
        # Add axes to the figure with the calculated properties
        ax = fig.add_axes([x_coords[ci], y_coords[ri],
                           x_fig, y_fig],
                          projection=proj)
        # Add geographic features to the plot
        ax = cgp.continentes_lon_lat(ax, **prop_grid)
        # Set the image extent and aspect ratio of the plot
        ax.set_extent(img_extent, proj)
        ax.set_aspect('auto')
        ax.set_title(f'{letras[ci][ri]}. {indieces[i]}', loc='left',
                     fontdict=font_prop)
        # Remove x-axis labels for subplots that are not in the last row
        if ri < (num_rows - 1):
            ax.set_xticklabels([])

        ds = ds_dic[indieces[ri]].median(dim='time')
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        var_values = ds[indieces[ri]].values

        cs = ax.pcolormesh(lon_values, lat_values, var_values,
                           cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                           transform=proj)
        ax.grid(False)
cbaxes = fig.add_axes([x_cbar, y_coords[ri], width_cbar, y_cbar])
fig.colorbar(cs, cax=cbaxes, orientation='vertical',
             label=label)


# -----------------------------------------------------------------------------
# Fila: 2 y 3, Columna 0. 'TX90p', 'TX10p'
# -----------------------------------------------------------------------------

indieces = ['TX90p', 'TX10p']
levels = np.linspace(6, 14, 9)
label = '% days/year'
cmap = 'viridis'
x_cbar = x_cbar_0
for i, ri in enumerate([2, 3]):
    for ci in [0]:
        # Add axes to the figure with the calculated properties
        ax = fig.add_axes([x_coords[ci], y_coords[ri],
                           x_fig, y_fig],
                          projection=proj)
        # Add geographic features to the plot
        ax = cgp.continentes_lon_lat(ax, **prop_grid)
        # Set the image extent and aspect ratio of the plot
        ax.set_extent(img_extent, proj)
        ax.set_aspect('auto')
        ax.set_title(f'{letras[ci][ri]}. {indieces[i]}', loc='left',
                     fontdict=font_prop)
        # Remove x-axis labels for subplots that are not in the last row
        if ri < (num_rows - 1):
            ax.set_xticklabels([])

        ds = ds_dic[indieces[i]].median(dim='time')
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        var_values = ds[indieces[i]].values

        cs = ax.pcolormesh(lon_values, lat_values, var_values,
                           cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                           transform=proj)
        ax.grid(False)

cbaxes = fig.add_axes([x_cbar, y_coords[ri], width_cbar, y_cbar])
fig.colorbar(cs, cax=cbaxes, orientation='vertical',
             label=label)

# -----------------------------------------------------------------------------
# Fila: 2 y 3, Columna 1. 'TX90p', 'TX10p'
# -----------------------------------------------------------------------------

indieces = ['TN90p', 'TN10p']
levels = np.linspace(6, 14, 9)
label = '% days/year'
cmap = 'viridis'
x_cbar = x_cbar_1
for i, ri in enumerate([2, 3]):
    for ci in [1]:
        # Add axes to the figure with the calculated properties
        ax = fig.add_axes([x_coords[ci], y_coords[ri],
                           x_fig, y_fig],
                          projection=proj)
        # Add geographic features to the plot
        ax = cgp.continentes_lon_lat(ax, **prop_grid)
        # Set the image extent and aspect ratio of the plot
        ax.set_extent(img_extent, proj)
        ax.set_aspect('auto')
        ax.set_title(f'{letras[ci][ri]}. {indieces[i]}', loc='left',
                     fontdict=font_prop)
        # Remove x-axis labels for subplots that are not in the last row
        if ri < (num_rows - 1):
            ax.set_xticklabels([])

        ds = ds_dic[indieces[i]].median(dim='time')
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        var_values = ds[indieces[i]].values

        cs = ax.pcolormesh(lon_values, lat_values, var_values,
                           cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                           transform=proj)
        ax.grid(False)

cbaxes = fig.add_axes([x_cbar, y_coords[ri], width_cbar, y_cbar])
fig.colorbar(cs, cax=cbaxes, orientation='vertical',
             label=label)


# -----------------------------------------------------------------------------
# Fila: 4, Columna 0. 'DTR'
# -----------------------------------------------------------------------------

indieces = ['DTR']
levels = np.linspace(6, 18, 9)
label = '°C'
cmap = sns.color_palette("Spectral_r", as_cmap=True)
x_cbar = x_cbar_0
for i, ri in enumerate([4]):
    for ci in [0]:
        # Add axes to the figure with the calculated properties
        ax = fig.add_axes([x_coords[ci], y_coords[ri],
                           x_fig, y_fig],
                          projection=proj)
        # Add geographic features to the plot
        ax = cgp.continentes_lon_lat(ax, **prop_grid)
        # Set the image extent and aspect ratio of the plot
        ax.set_extent(img_extent, proj)
        ax.set_aspect('auto')
        ax.set_title(f'{letras[ci][ri]}. {indieces[i]}', loc='left',
                     fontdict=font_prop)
        # Remove x-axis labels for subplots that are not in the last row
        if ri < (num_rows - 1):
            ax.set_xticklabels([])

        ds = ds_dic[indieces[i]].median(dim='time')
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        var_values = ds[indieces[i]].values

        cs = ax.pcolormesh(lon_values, lat_values, var_values,
                           cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                           transform=proj)
        ax.grid(False)

cbaxes = fig.add_axes([x_cbar, y_coords[ri], width_cbar, y_fig])
fig.colorbar(cs, cax=cbaxes, orientation='vertical',
             label=label)

# -----------------------------------------------------------------------------
# Fila: 4, Columna 0. 'DTR'
# -----------------------------------------------------------------------------

indieces = ['WSDI']
levels = np.linspace(0, 30, 13)
label = 'days/year'
cmap = sns.color_palette("Spectral_r", as_cmap=True)
x_cbar = x_cbar_1
for i, ri in enumerate([4]):
    for ci in [1]:
        # Add axes to the figure with the calculated properties
        ax = fig.add_axes([x_coords[ci], y_coords[ri],
                           x_fig, y_fig],
                          projection=proj)
        # Add geographic features to the plot
        ax = cgp.continentes_lon_lat(ax, **prop_grid)
        # Set the image extent and aspect ratio of the plot
        ax.set_extent(img_extent, proj)
        ax.set_aspect('auto')
        ax.set_title(f'{letras[ci][ri]}. {indieces[i]}', loc='left',
                     fontdict=font_prop)
        # Remove x-axis labels for subplots that are not in the last row
        if ri < (num_rows - 1):
            ax.set_xticklabels([])

        ds = ds_dic[indieces[i]].median(dim='time')
        lat_values = ds.lat.values
        lon_values = ds.lon.values
        var_values = ds[indieces[i]].values

        cs = ax.pcolormesh(lon_values, lat_values, var_values,
                           cmap=cmap, vmin=levels.min(), vmax=levels.max(),
                           transform=proj)
        ax.grid(False)

cbaxes = fig.add_axes([x_cbar, y_coords[ri], width_cbar, y_fig])
fig.colorbar(cs, cax=cbaxes, orientation='vertical',
             label=label)


# %%
path_fig = '/home/cambio_climatico/Act_3/figures/Indices/ERA5/'
fig.savefig(f'{path_fig}Temp_indexes_ERA5_America_{time_range}.png', dpi=200,
            bbox_inches='tight', transparent=False,
            facecolor='white')

fig.savefig(f'{path_fig}Temp_indexes_ERA5_America_{time_range}.pdf',
            bbox_inches='tight', transparent=False,
            facecolor='white')
# %%
