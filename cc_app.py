"""
Created on 24-April-2024
@author: jdmantillaq
"""

# import plotly.express as px
# import pandas as pd
# import numpy as np
import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_leaflet as dl
import dash_daq as daq
from pathlib import Path
import seaborn as sns
from properties import index_prop
# Define external CSS stylesheet URLs
dbc_css = \
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Initialize the Dash application with Zephyr theme and external CSS stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc_css])

# Set the title of the Dash application
app.title = 'Cambio Climático'

# Load Zephyr figure template
load_figure_template("zephyr")

# Define styles for sliders, text, and colorbars
slider_style = {"font-size": "18px",
                'margin-top': '20px', 'left-right': '30px'}
text_style = {"font-size": "20px"}
colorbar_style = {"font-size": "20px", 'color': 'black'}

# Path to assets directory
path_asses = './assets/'
# Image extent
img_extent = (-115+360,  -10, -30+360, 30)
# Image bounds
image_bounds = [[-10-0.375, -115], [30-0.375, -30]]

# alpha Image Overlay
alpha_overlay = 0.75


keys = ["alidade_smooth", "stamen_toner_lite"]
url = "https://tiles.stadiamaps.com/tiles/{}/{{z}}/{{x}}/{{y}}{{r}}.png"
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

# map_layer = dl.LayersControl([dl.BaseLayer(dl.TileLayer(url=url.format(key),
#                                        attribution=attribution),
#                           name=key, checked=key == keys[0]) for key in keys])

map_layer = dl.TileLayer(url=url.format(keys[0]), attribution=attribution)


# Basic map content
map_content_basic = [
    map_layer,
    dl.FullScreenControl(),  # Add full screen control
    dl.ScaleControl(position="bottomright")  # Add scale control
]

# Define the layout of the Dash application
map_dl = app.layout = html.Div([
    dl.Map(
        id='map',  # Map component ID
        children=map_content_basic,  # Map children
        zoom=4.5,  # Initial zoom level
        center=(6.248011, -75.577277),  # Initial center coordinates
        style={'width': '100%',  # Map style
               'height': '73vh',
               'margin': "auto",
               "display": "block"}
    )
])


# -----------------------------------------------------------------------------
# popover Datasets
# -----------------------------------------------------------------------------

# Define the list of models for the NEX dataset
models_NEX = ['ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CanESM5',
              'CMCC-CM2-SR5', 'CMCC-ESM2', 'EC-Earth3',
              'EC-Earth3-Veg-LR', 'GFDL-CM4',
              'GFDL-ESM4', 'INM-CM4-8', 'INM-CM5-0',
              'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6',
              'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NESM3',
              'NorESM2-LM', 'NorESM2-MM', 'TaiESM1']

# Subset of models for the NEX dataset
models_NEX = ['BCC-CSM2-MR', 'MIROC6', 'MPI-ESM1-2-LR',  'MRI-ESM2-0',
              'NorESM2-LM']

# Define the list of models for the HighResMIP dataset
models_HighResp = ['FGOALS-f3-L', 'MRI-AGCM3-2-H',
                   'MRI-AGCM3-2-S', 'NICAM16-7S', 'NICAM16-8S']

models_HighResp = ['MRI-AGCM3-2-S']

# Define the list of observational datasets
obs_list = ['ERA5', 'CHIRPS']

# Define radio items for observational dataset selection
radioitems_dataset_obs = dbc.CardBody(dcc.RadioItems(obs_list,
                                                     id="radio_dataset_obs",),
                                      style=slider_style)

# Define radio items for NEX-GDDP-CMIP6 dataset selection
radioitems_dataset_NEX = dbc.CardBody(dcc.RadioItems(models_NEX,
                                                     id="radio_dataset_NEX",),
                                      style=slider_style)

# Define radio items for HighResMIP-CMIP6 dataset selection
radioitems_dataset_HighResp = dbc.CardBody(
    dcc.RadioItems(models_HighResp,
                   id="radio_dataset_HighResp",),
    style=slider_style)

# Define the content for dataset selection popover
content_dataset = dbc.PopoverBody(
    children=[dbc.Row([dbc.Col([html.H3(children="Histórico")], width=6),
                       dbc.Col([html.H3(children="Proyecciones")], width=6)]),
              html.Hr(),
              dbc.Row([dbc.Col([html.H5(children="Observaciones")], width=4),
                       dbc.Col([html.H5(children="NEX-GDDP-CMIP6")], width=4),
                       dbc.Col([html.H5(children="HighResMIP-CMIP6")],
                               width=4),
                       ]),
              html.Hr(),
              dbc.Row([dbc.Col([radioitems_dataset_obs], width=4),
                       dbc.Col([radioitems_dataset_NEX], width=4),
                       dbc.Col([radioitems_dataset_HighResp], width=4),
                       ])])

# Define the button and popover for dataset selection
popovers_dataset = html.Div(
    [
        dbc.Button(
            "Dataset",
            id="button_dataset",
            n_clicks=0,
            style=slider_style
        ),
        dbc.Popover(
            [dbc.PopoverHeader("Seleccione un conjunto de datos"),
             dbc.PopoverBody(content_dataset),
             ],
            target="button_dataset",
            placement='bottom',
            trigger="legacy",
            autohide=True,
            style={'maxWidth': '3000px'},
            body=True,
        ),
    ]
)

# -----------------------------------------------------------------------------
# popover extreme indexes
# -----------------------------------------------------------------------------

# Define lists of temperature and precipitation indices
tas_index_list = ['TXx', 'TXn', 'TNx', 'TNn', 'TX90p', 'TX10p', 'TN90p',
                  'TN10p', 'DTR', 'WSDI']

pr_index_list = ['R5mm', 'R10mm', 'R20mm', 'R50mm', 'CDD', 'CWD', 'R95p',
                 'R99p', 'PRCPTOT', 'SDII', 'P75y', 'P90y', 'P95y']

# Define radio items for temperature variable selection
radioitems_var_tas = dbc.CardBody(dcc.RadioItems(tas_index_list,
                                                 id="radio_var_tas",
                                                 value=None),
                                  style=slider_style)

# Define radio items for precipitation variable selection
radioitems_var_pr = dbc.CardBody(dcc.RadioItems(pr_index_list,
                                                id="radio_var_pr",),
                                 style=slider_style)

# Define the content for variable selection popover
content_variable = dbc.PopoverBody(
    style={
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "space-between"
    },
    children=[
        dbc.Col([html.H5(children="Temperatura"),  # Temperature heading
                 html.Hr(),  # Horizontal line
                 radioitems_var_tas], width=7),  # Radio items for temperature
        dbc.Col([html.H5(children="Precipitación"),  # Precipitation heading
                 html.Hr(),  # Horizontal line
                 radioitems_var_pr], width=7),  # Radio items for precipitation
    ]
)

# Define dropdown menus for temperature and precipitation indices
dropdown_tas_index = dbc.DropdownMenu(
    label="Temperatura",  # Dropdown label for temperature
    children=radioitems_var_tas,  # Radio items for temperature
    color="info",  # Color of the dropdown menu
    size="lg",  # Size of the dropdown menu
    id='dropdown_tas'  # ID of the dropdown menu
)

dropdown_pr_index = dbc.DropdownMenu(
    label="Precipitación",  # Dropdown label for precipitation
    children=radioitems_var_pr,  # Radio items for precipitation
    color="info",  # Color of the dropdown menu
    size="lg",  # Size of the dropdown menu
    id='dropdown_pr'  # ID of the dropdown menu
)

# Define the content for variable selection popover
text_description = \
    '''
Descripción del ínidice seleccionado
'''

# Define the content for variable selection popover
popover_body_content = [
    dbc.Row(dcc.Markdown(id='description_index', children=text_description),
            style={"height": "5rem", "width": "28rem",
                   "font-size": "16.5px"}),
    # html.Hr(),
    dbc.Row(
        [dbc.Col(dropdown_tas_index),  # Column for temperature dropdown menu
         dbc.Col(dropdown_pr_index),  # Column for precipitation dropdown menu
         ],
        justify="between",),
    # html.Br(),
]

content_variable = dbc.PopoverBody(
    children=popover_body_content  # Populate popover body with dropdown menus
)

# Define the button and popover for variable selection
popovers_variable = html.Div(
    [
        dbc.Button(
            "Indices de Extremos",  # Button label for extreme indices
            id="button_variable",  # ID of the button
            n_clicks=0,  # Initial number of clicks
            style=slider_style  # Style for the button
        ),
        dbc.Popover(
            [
                # Popover header
                dbc.PopoverHeader("Seleccione el índice a graficar"),
                # Popover body with variable selection content
                dbc.PopoverBody(content_variable),
            ],
            target="button_variable",  # Target ID for the popover
            placement='bottom',  # Placement of the popover
            trigger="legacy",  # Trigger for the popover
            autohide=True,  # Autohide option for the popover
            style={'maxWidth': '500px'},  # Maximum width of the popover
            body=True,  # Render as body
        ),
    ]
)


# -----------------------------------------------------------------------------
# popover time period
# -----------------------------------------------------------------------------

# Define lists of historical and projected time periods and scenarios
hist_time_tas = ['1979-2014']  # Historical time period for temperature
hist_time_pr = ['1981-2014']  # Historical time period for precipitation
hist_time_proj = ['2021-2040', '2041-2060', '2061-2080', '2081-2100']
# Projected time periods
scenarios = ['SSP2-4.5', 'SSP5-8.5']  # Scenarios

scenarios_HighResMIP = ['RCP8.5']

# Define radio items for historical and projected time periods
radioitems_time_hist = dbc.CardBody(dcc.RadioItems(options=hist_time_proj,
                                                   id="radio_time_hist"),
                                    style=slider_style)

# Define radio items for scenario selection
radioitems_scenario = dbc.CardBody(dcc.RadioItems(scenarios,
                                                  id="radio_scenario",
                                                  value=scenarios[0]),
                                   style=slider_style)

# Define toggle switch for quantity/value selection
toogle_quantity = daq.ToggleSwitch(
    id='toogle_quantity',
    size=60,
    value=True,
    label=['Cambio (°C)', 'Valor (°C)'],
    style={'font-size': '32px'}
)

# Define content for conditional observation display
content_conditional_obs = [
    dbc.Row([dbc.Col(html.H5(children="Cantidad"), width=5),
             dbc.Col(toogle_quantity, width=7)]),
    html.Hr(),
    dbc.Row([dbc.Col([html.H5(children="Observaciones")], width=6),
             dbc.Col([html.H5(children="Periodo")], width=6)]),
    html.Hr(),
    dbc.Row([dbc.Col([radioitems_scenario], width=6),
             dbc.Col([radioitems_time_hist], width=6)])]

# Define content for conditional model display
content_conditional_models = [
    dbc.Row([dbc.Col(html.H5(children="Cantidad"), width=5),
             dbc.Col(toogle_quantity, width=7)]),
    html.Hr(),
    dbc.Row([dbc.Col([html.H5(children="Escenario")], width=6),
             dbc.Col([html.H5(children="Periodo")], width=6)]),
    html.Hr(),
    dbc.Row([dbc.Col([radioitems_scenario], width=6),
             dbc.Col([radioitems_time_hist], width=6)])]

# Define content for time period selection popover
content_time_period = dbc.PopoverBody(
    children=content_conditional_obs,
    id='popup_quantity_period')

# Define popover for time period selection
popovers_time_period = html.Div(
    [
        dbc.Button(
            "Cantidad/Periodo de estudio",
            id="button_time_period",  # ID of the button
            n_clicks=0,  # Initial number of clicks
            style=slider_style  # Style for the button
        ),
        dbc.Popover(
            [dbc.PopoverHeader(
                "Seleccione la cantidad y el periodo de estudio"),
             dbc.PopoverBody(content_time_period),
             ],
            target="button_time_period",  # Target ID for the popover
            placement='bottom',  # Placement of the popover
            trigger="legacy",  # Trigger for the popover
            autohide=True,  # Autohide option for the popover
            style={'maxWidth': '1000px'},  # Maximum width of the popover
            body=True,  # Render as body
        ),
    ]
)


# -----------------------------------------------------------------------------
# Tab 1: content
# -----------------------------------------------------------------------------


tab1_content = dbc.Card(
    dbc.CardBody(
        [dbc.Row([dbc.Col([popovers_dataset, popovers_variable,
                           popovers_time_period],
                          style={"display": "flex", "flexWrap": "wrap"})]),
         dbc.Row(map_dl),
         html.H4(children="",
                 style={"padding": "10px", "text-align": "center"},
                 id='title_page'),]
    ))


# -----------------------------------------------------------------------------
# Tab 1: content
# -----------------------------------------------------------------------------


tab2_content = dbc.Card()


app.layout = html.Div(
    [dcc.Store(id='toogle_quantity_state', data=True),
        html.Div(
        className="header",
        children=[
            html.Div(
                className="div-info",
                children=[
                    html.H4(children="Cambio Climático",
                            style={"padding": "10px"}),
                    # html.Hr(),
                    dbc.Tabs([
                        dbc.Tab(tab1_content, label="Índices de Extremos",
                                tab_id="tab-1")],
                             id="tabs",
                             active_tab="tab-1",
                             )
                ],
            ),
        ],
    ),
    ], style=text_style
)

# -----------------------------------------------------------------------------
# Toogle-State
# -----------------------------------------------------------------------------

# Callback to update state based on user interaction with toogle_quantity


@app.callback(
    Output('toogle_quantity_state', 'data'),
    Input('toogle_quantity', 'value')
)
def update_state(toogle_value):
    return toogle_value

# -----------------------------------------------------------------------------
# Dataset
# -----------------------------------------------------------------------------
# Define callback to clear selections for dataset radio items


@app.callback(
    [Output("radio_dataset_obs", "value"),
     Output("radio_dataset_NEX", "value"),
     Output("radio_dataset_HighResp", "value")],
    [Input("radio_dataset_obs", "value"),
     Input("radio_dataset_NEX", "value"),
     Input("radio_dataset_HighResp", "value")]
)
def clear_selections_dataset(obs_value, nex_value, high_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [None, None, None]
    else:
        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'radio_dataset_obs':
            return [obs_value, None, None]
        elif prop_id == 'radio_dataset_NEX':
            return [None, nex_value, None]
        elif prop_id == 'radio_dataset_HighResp':
            return [None, None, high_value]
        else:
            return [None, None, None]

# -----------------------------------------------------------------------------
# Indices
# -----------------------------------------------------------------------------

# Define callback to clear selections for variable radio items


@app.callback(
    [Output("radio_var_tas", "value"),
     Output("radio_var_pr", "value")],
    [Input("radio_var_tas", "value"),
     Input("radio_var_pr", "value")]
)
def clear_selections_var(value_1, value_2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [None, None]
    else:
        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'radio_var_tas':
            return [value_1, None]
        elif prop_id == 'radio_var_pr':
            return [None, value_2]
        else:
            return [None, None]


@app.callback(
    Output("description_index", "children"),
    [Input("radio_var_tas", "value"),
     Input("radio_var_pr", "value")]
)
def update_index_description(tas_value, pr_value):
    if not any([tas_value, pr_value]):
        raise PreventUpdate
    if tas_value is not None:
        index = tas_value
    else:
        index = pr_value

    text = f'**{index}**: {index_prop[index]["description"]}'
    return text

# -----------------------------------------------------------------------------
# Extreme Index conditional
# -----------------------------------------------------------------------------


def create_possible_options(lst, disabled=False):
    color = 'grey' if disabled else 'black'
    font_size = 15 if disabled else 16

    return [{'label': i, 'style': {'color': color,
                                   'font-size': f"{font_size}px"},
             'value': i, 'disabled': disabled} for i in lst]

#  Define callback to disable the index buttoms options


@app.callback(
    [
        #  Output("radio_var_tas", "options"),
        #  Output("radio_var_pr", "options"),
        Output("dropdown_tas", "disabled"),
        Output("dropdown_pr", "disabled")],
    [Input("radio_dataset_obs", "value"),
     Input("radio_dataset_NEX", "value"),
     Input("radio_dataset_HighResp", "value")]
)
def filter_index_available(obs_value, nex_value, high_value):
    if not any([obs_value, nex_value, high_value]):
        raise PreventUpdate

    options_tas_disabled = options_pr_disabled = False
    if obs_value is not None:
        options_tas_disabled = obs_value == 'CHIRPS'
        options_pr_disabled = obs_value == 'ERA5'

    else:
        options_tas_disabled = options_pr_disabled = False

    # options_tas = create_possible_options(tas_index_list,
    #                                       disabled=options_tas_disabled)
    # options_pr = create_possible_options(pr_index_list,
    #                                      disabled=options_pr_disabled)
    return options_tas_disabled, options_pr_disabled


# -----------------------------------------------------------------------------
# Popup/Toggle Quantity conditional
# -----------------------------------------------------------------------------

#  Define callback change the quantity plotted
@app.callback(
    [Output("toogle_quantity", "label"),
     Output("toogle_quantity", "value")],
    [Input("radio_dataset_obs", "value"),
     Input("radio_var_tas", "value"),
     Input("radio_var_pr", "value"),
     # Input("toogle_quantity", "value"),
     Input('toogle_quantity_state', 'data')]
)
def change_toogle_labels(obs_value, tas_value, pr_value, on):
    if not any([obs_value, tas_value, pr_value]):
        raise PreventUpdate

    word_left = 'Cambio'
    word_units_left_2 = ''
    word_right = 'Valor'
    units = '°C'

    if obs_value is not None:
        word_left = 'Tendencia'
        word_units_left_2 = '/decada'
    if tas_value is not None:
        units = index_prop[tas_value]['units']
    elif pr_value is not None:
        units = index_prop[pr_value]['units']
    label = [f'{word_left} ({units}{word_units_left_2})',
             f'{word_right} ({units})']
    return label, on

# Define callback to change the content of the Popup quantity


@app.callback(
    Output("popup_quantity_period", "children"),
    [Input("radio_dataset_obs", "value"),
     Input("radio_dataset_NEX", "value"),
     Input("radio_dataset_HighResp", "value")]
)
def change_content_popup_quantity_period(obs_value, nex_value, high_value):
    if not any([obs_value, nex_value, high_value]):
        raise PreventUpdate

    if obs_value is not None:
        return content_conditional_obs
    else:
        return content_conditional_models

# Define callback to change the period time range in the popover content


@app.callback(
    [Output("radio_scenario", "options"),
     Output("radio_scenario", "value"),
     Output("radio_time_hist", "options"),
     Output("radio_time_hist", "value")],

    [Input("radio_dataset_obs", "value"),
     Input("radio_dataset_NEX", "value"),
     Input("radio_dataset_HighResp", "value")]
)
def change_options_period(obs_value, nex_value, high_value):
    if obs_value == 'ERA5':
        return [], 'historical', hist_time_tas, hist_time_tas[0],
    if obs_value == 'CHIRPS':
        return [], 'historical', hist_time_pr, hist_time_pr[0],

    if any([nex_value]):
        return scenarios, scenarios[0], hist_time_proj, hist_time_proj[0]
    if any([high_value]):
        return scenarios_HighResMIP, scenarios_HighResMIP[0], \
            hist_time_proj, hist_time_proj[0]

    else:
        raise PreventUpdate


# -----------------------------------------------------------------------------
# Map Callbacks
# -----------------------------------------------------------------------------

# Define callback to update the map content


@app.callback(
    [Output("title_page", "children"),
     Output("map", "children")],
    [
        Input("radio_dataset_obs", "value"),
        Input("radio_dataset_NEX", "value"),
        Input("radio_dataset_HighResp", "value"),
        Input("radio_var_tas", "value"),
        Input("radio_var_pr", "value"),
        Input("radio_time_hist", "value"),
        Input("radio_scenario", "value"),
        Input("toogle_quantity", "value")

    ],
)
def verify_components(obs_value, nex_value, high_value, tas_value, pr_value,
                      time_hist_value, radio_scenario, toogle_val):
    # Combine data selection logic
    data_part = obs_value or nex_value or high_value

    if not any([data_part]):
        raise PreventUpdate

    # Combine index selection logic
    index_part = tas_value or pr_value
    if not any([index_part]):
        raise PreventUpdate

    projection = False
    if any([nex_value, high_value]):
        projection = True
        if nex_value is not None:
            source = 'NEX-GDDP-CMIP6'
        else:
            source = 'HighResMIP-CMIP6'

    source = f'{source}: ' if projection else ''
    scenario = radio_scenario if radio_scenario else ""
    (toogle_quantity, str_values) = ('trend', 'Tendencia') if obs_value is not\
        None else ('anom', 'Anomalías')

    quantity = 'value' if toogle_val else f'{toogle_quantity}'
    str_values = 'Valor medio' if toogle_val else str_values
    prefix_trend = '' if toogle_val else f'_{toogle_quantity}'

    name_file = f'{data_part}_{index_part}{prefix_trend}_{scenario}_'\
        f'{time_hist_value}.png'
    file_path = f"{path_asses}{name_file}"

    # file_exists = "File exists!" if Path(
    #     file_path).exists() else "File doesn't exist!"

    units = index_prop[index_part]['units']
    if quantity == 'trend':
        units += '/decada'

    if scenario == 'historical':
        scenario = 'Histórico'
    # Construct the title with proper formatting
    title = f"{source}{data_part} | {index_part} ({units}) | {str_values} | "\
        f"{scenario}: {time_hist_value}"

    if not Path(file_path).exists():
        return title, map_content_basic

    map_content_updated = update_map(index_part, file_path, value=quantity,
                                     projection=projection)

    return title, map_content_updated

# Define function to load the map content; ImageOverlay and Colorbar


def update_map(index, file, value='value', projection=False):

    units = index_prop[index]['units']
    if value == 'value':
        cmap = index_prop[index]['cmap']
        if projection:
            levels = index_prop[index]['var_values_proj']
        else:
            levels = index_prop[index]['var_values']

    elif value == 'trend':
        cmap = index_prop[index]['cmap_trend']
        levels = index_prop[index]['trend_values']
        units += '/decada'
    else:
        if projection:
            levels = index_prop[index]['anom_values_proj']
            cmap = index_prop[index]['cmap_anom_proj']
        else:
            levels = index_prop[index]['anom_values']
            cmap = index_prop[index]['cmap_anom']

    colorscale = sns.palettes.color_palette(cmap).as_hex()
    map_content = [
        map_layer,

        dl.FullScreenControl(),
        dl.ImageOverlay(id='image-overlay',
                        opacity=alpha_overlay,
                        url=file,
                        bounds=image_bounds),
        dl.ScaleControl(position="bottomright"),
        dl.Colorbar(id='colorbar',
                    colorscale=colorscale,
                    width=20,
                    height=250,
                    nTicks=5,
                    style=colorbar_style,
                    min=levels[0],
                    max=levels[-1],
                    position="bottomleft",
                    tooltip=True,
                    unit=units)]
    return map_content


app.run_server(port=2100, host='0.0.0.0')
