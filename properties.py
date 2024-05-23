import numpy as np

index_prop = {
    # Indices de Precipitación
    'R5mm': {'var_values': np.linspace(0, 250),
             'var_values_proj': np.linspace(0, 250),
             'anom_values': np.linspace(-30, 30),
             'anom_values_proj': np.linspace(-30, 30),
             'trend_values': np.linspace(-15, 15),
             'cmap': 'viridis',
             'cmap_anom': 'RdBu',
             'cmap_anom_proj': 'RdBu',
             'cmap_trend': 'RdBu',
             'units': 'días/año'},

    'R10mm': {'var_values': np.linspace(0, 250),
              'var_values_proj': np.linspace(0, 250),
              'anom_values': np.linspace(-30, 30),
              'anom_values_proj': np.linspace(-30, 30),
              'trend_values': np.linspace(-15, 15),
              'cmap': 'viridis',
              'cmap_anom': 'RdBu',
              'cmap_anom_proj': 'RdBu',
              'cmap_trend': 'RdBu',
              'units': 'días/año'},

    'R20mm': {'var_values': np.linspace(0, 150),
              'var_values_proj': np.linspace(0, 150),
              'anom_values': np.linspace(-30, 30),
              'anom_values_proj': np.linspace(-30, 30),
              'trend_values': np.linspace(-8, 8),
              'cmap': 'viridis',
              'cmap_anom': 'RdBu',
              'cmap_anom_proj': 'RdBu',
              'cmap_trend': 'RdBu',
              'units': 'días/año'},

    'R50mm': {'var_values': np.linspace(0, 30),
              'var_values_proj': np.linspace(0, 30),
              'anom_values': np.linspace(-30, 30),
              'anom_values_proj': np.linspace(-8, 8),
              'trend_values': np.linspace(-4, 4),
              'cmap': 'viridis',
              'cmap_anom': 'RdBu',
              'cmap_anom_proj': 'RdBu',
              'cmap_trend': 'RdBu',
              'units': 'días/año'},

    'CDD': {'var_values': np.linspace(0, 60),
            'var_values_proj': np.linspace(0, 200),
            'anom_values': np.linspace(-10, 10),
            'anom_values_proj': np.linspace(-75, 75),
            'trend_values': np.linspace(-10, 10),
            'cmap_trend': 'RdBu_r',
            'cmap_anom': 'RdBu_r',
            'cmap_anom_proj': 'RdBu_r',
            'cmap': 'plasma',
            'units': 'días/año'},

    'CWD': {'var_values': np.linspace(0, 60),
            'var_values_proj': np.linspace(0, 100),
            'anom_values': np.linspace(-10, 10),
            'anom_values_proj': np.linspace(-20, 20),
            'trend_values': np.linspace(-5, 5),
            'cmap_trend': 'RdBu',
            'cmap_anom': 'RdBu',
            'cmap_anom_proj': 'RdBu_r',
            'cmap': 'plasma',
            'units': 'días/año'},

    'R95p': {'var_values': np.linspace(0, 1000),
             'var_values_proj': np.linspace(0, 1000),
             'anom_values': np.linspace(-350, 350),
             'anom_values_proj': np.linspace(-400, 400),
             'trend_values': np.linspace(-200, 200),
             'cmap': "Spectral_r",
             'cmap_anom': 'BrBG',
             'cmap_anom_proj': 'BrBG',
             'cmap_trend': 'BrBG',
             'units': 'mm/año'},

    'R99p': {'var_values': np.linspace(0, 400),
             'var_values_proj': np.linspace(0, 400),
             'anom_values': np.linspace(-250, 250),
             'anom_values_proj': np.linspace(-300, 300),
             'trend_values': np.linspace(-200, 200),
             'cmap': "Spectral_r",
             'cmap_trend': 'BrBG',
             'cmap_anom': 'BrBG',
             'cmap_anom_proj': 'BrBG',
             'units': 'mm/año'},

    'PRCPTOT': {'var_values': np.linspace(0, 6000),
                'var_values_proj': np.linspace(0, 6000),
                'anom_values': np.linspace(-900, 900),
                'anom_values_proj': np.linspace(-900, 900),
                'trend_values': np.linspace(-200, 200),
                'cmap': "Spectral_r",
                'cmap_trend': 'BrBG',
                'cmap_anom': 'BrBG',
                'cmap_anom_proj': 'BrBG',
                'units': 'mm/año'},

    'SDII': {'var_values': np.linspace(0, 30),
             'var_values_proj': np.linspace(0, 30),
             'anom_values': np.linspace(-5, 5),
             'anom_values_proj': np.linspace(-5, 5),
             'trend_values': np.linspace(-2, 2),
             'cmap': "Spectral_r",
             'cmap_trend': 'BrBG',
             'cmap_anom': 'BrBG',
             'cmap_anom_proj': 'BrBG',
             'units': 'mm/día'},

    'P75y': {'var_values': np.linspace(0, 60),
             'var_values_proj': np.linspace(0, 60),
             'anom_values': np.linspace(-8, 8),
             'anom_values_proj': np.linspace(-5, 5),
             'trend_values': np.linspace(-4, 4),
             'cmap': "Spectral_r",
             'cmap_trend': 'BrBG',
             'cmap_anom': 'BrBG',
             'cmap_anom_proj': 'BrBG',
             'units': 'mm/día'},

    'P90y': {'var_values': np.linspace(0, 60),
             'var_values_proj': np.linspace(0, 60),
             'anom_values': np.linspace(-8, 8),
             'anom_values_proj': np.linspace(-5, 5),
             'trend_values': np.linspace(-4, 4),
             'cmap': "Spectral_r",
             'cmap_trend': 'BrBG',
             'cmap_anom': 'BrBG',
             'cmap_anom_proj': 'BrBG',
             'units': 'mm/día'},

    'P95y': {'var_values': np.linspace(0, 60),
             'var_values_proj': np.linspace(0, 60),
             'anom_values': np.linspace(-8, 8),
             'trend_values': np.linspace(-4, 4),
             'anom_values_proj': np.linspace(-5, 5),
             'cmap': "Spectral_r",
             'cmap_trend': 'BrBG',
             'cmap_anom': 'BrBG',
             'cmap_anom_proj': 'BrBG',
             'units': 'mm/día'},

    # Indices de Temperatura
    'TXx': {'var_values': np.linspace(18, 50),
            'var_values_proj': np.linspace(18, 50),
            'anom_values': np.linspace(-6, 6),
            'anom_values_proj': np.linspace(-8, 8),
            'trend_values': np.linspace(-1.2, 1.2),
            'cmap': 'Spectral_r',
            'cmap_anom': 'RdBu_r',
            'cmap_anom_proj': 'RdBu_r',
            'cmap_trend': 'RdBu_r',
            'units': '°C'},

    'TXn': {'var_values': np.linspace(10, 30),
            'var_values_proj': np.linspace(10, 30),
            'anom_values': np.linspace(-6, 6),
            'anom_values_proj': np.linspace(-6, 6),
            'trend_values': np.linspace(-1.2, 1.2),
            'cmap': 'Spectral_r',
            'cmap_anom': 'RdBu_r',
            'cmap_anom_proj': 'RdBu_r',
            'cmap_trend': 'RdBu_r',
            'units': '°C'},

    'TNx': {'var_values': np.linspace(6, 32),
            'var_values_proj': np.linspace(6, 50),
            'anom_values': np.linspace(-6, 6),
            'anom_values_proj': np.linspace(-6, 6),
            'trend_values': np.linspace(-1.2, 1.2),
            'cmap': 'Spectral_r',
            'cmap_anom': 'RdBu_r',
            'cmap_anom_proj': 'RdBu_r',
            'cmap_trend': 'RdBu_r',
            'units': '°C'},

    'TNn': {'var_values': np.linspace(6, 32),
            'var_values_proj': np.linspace(6, 40),
            'anom_values': np.linspace(-6, 6),
            'anom_values_proj': np.linspace(-6, 6),
            'trend_values': np.linspace(-1.2, 1.2),
            'cmap': 'Spectral_r',
            'cmap_anom': 'RdBu_r',
            'cmap_anom_proj': 'RdBu_r',
            'cmap_trend': 'RdBu_r',
            'units': '°C'},

    'TX90p': {'var_values': np.linspace(0, 12),
              'var_values_proj': np.linspace(0, 100),
              'anom_values': np.linspace(-90, 90),
              'anom_values_proj': np.linspace(0, 100),
              'trend_values': np.linspace(-5, 5),
              'cmap': 'hot_r',
              'cmap_anom': 'RdBu_r',
              'cmap_anom_proj': 'Reds',
              'cmap_trend': 'RdBu_r',
              'units': '% días/año'},
    
    'TX10p': {'var_values': np.linspace(0, 12),
              'var_values_proj':  np.linspace(0, 12),
              'anom_values': np.linspace(-15, 15),
              'anom_values_proj': np.linspace(-10, 10),
              'trend_values': np.linspace(-5, 5),
              'cmap': 'RdYlBu',
              'cmap_anom': 'RdBu',
              'cmap_anom_proj': 'RdBu',
              'cmap_trend': 'RdBu',
              'units': '% días/año'},

    'TN90p': {'var_values': np.linspace(0, 12),
              'var_values_proj': np.linspace(0, 100),
              'anom_values': np.linspace(-80, 80),
              'anom_values_proj': np.linspace(0, 100),
              'trend_values': np.linspace(-5, 5),
              'cmap': 'hot_r',
              'cmap_anom': 'RdBu_r',
              'cmap_anom_proj': 'Reds',
              'cmap_trend': 'RdBu_r',
              'units': '% días/año'},

    'TN10p': {'var_values': np.linspace(0, 10),
              'var_values_proj': np.linspace(0, 10),
              'anom_values': np.linspace(-10, 10),
              'anom_values_proj': np.linspace(-10, 10),
              'trend_values': np.linspace(-5, 5),
              'cmap': 'RdYlBu',
              'cmap_anom': 'RdBu',
              'cmap_anom_proj': 'RdBu',
              'cmap_trend': 'RdBu',
              'units': '% días/año'},

    'DTR': {'var_values': np.linspace(6, 18),
            'var_values_proj': np.linspace(6, 18),
            'anom_values': np.linspace(-1, 1),
            'anom_values_proj': np.linspace(-1.5, 1.5),
            'trend_values': np.linspace(-1, 1),
            'cmap': 'Spectral_r',
            'cmap_anom': 'RdBu_r',
            'cmap_anom_proj': 'RdBu_r',
            'cmap_trend': 'RdBu_r',
            'units': '°C'},

    'WSDI': {'var_values': np.linspace(0, 30),
             'var_values_proj': np.linspace(0, 365),
             'anom_values': np.linspace(-250, 250),
             'anom_values_proj': np.linspace(0, 250),
             'trend_values': np.linspace(-15, 15),
             'cmap': 'plasma',
             'cmap_anom': 'RdBu_r',
             'cmap_anom_proj': 'Reds',
             'cmap_trend': 'RdBu_r',
             'units': 'días/año'},
}
