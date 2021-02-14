""""
Finally an excuse to learn to make dash apps!
Created for the Advanced Scripting Course 2021 to show
  1) scientific output from a work flow that includes the skills learnt in the course (bash scripting, SLURM)
  2) the objectives of my project
  3) how the HPC and automation using bash will be indispensible for the remaining workflow of my project
  4) application of the git course by pushing this app..
"""

import glob

import numpy as np
import xarray as xr

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = dash.Dash()
colors = {
    'background': '#3a0c10',
    'header-text': '#dbb000',
    'text': '#f2d1b5'
}
default_text_style = {"color": colors['text']}
menu_header_text_style = default_text_style
menu_options_text_style = default_text_style

# Set up the app layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='ADVANCED SCRIPTING FOR DROUGHT RESILIENCE',
        style={
            'textAlign': 'center',
            'color': colors['header-text']
        }
    ),
    html.Div(children='Nele Reyniers, University of East Anglia', style={
        'textAlign': 'center',
        'color': colors['header-text']
    }),
    # select whether to show spi or spei, make spi default
    html.Label('Drought index: ', style=menu_header_text_style),
    dcc.RadioItems(id="standardized_index",
                   options=[
                       {'label': 'Standardized Precipitation Index (SPI)', 'value': 'spi'},
                       {'label': 'Standardized Preciptiation Evaporation Index (SPEI)', 'value': 'spei'}
                   ],
                   value='spi', style=menu_options_text_style
    ),
    # select ensemble member to show
    html.Label('UKCP18 Perturbed Parameter Ensemble RCM member:', style=menu_header_text_style),
    dcc.Dropdown(id="ensemble_member",
        options=[{'label': 'ensemble member 1 (STD)', 'value': 1}] +
                [{'label': f'ensemble member {i}', 'value': i} for i in range(4, 14)] +
                [{'label': f'Eensemble member 15', 'value': 15}],
        value=1, style=menu_options_text_style
    ),
    # select period to show
    html.Label('Drought index aggregation level in months:', style=menu_header_text_style),
    dcc.Dropdown(id="agg_lvl_in_months",
        options=[{'label': '1', 'value': 1},
                 {'label': '3', 'value': 3},
                 {'label': '6', 'value': 6},
                 {'label': '12', 'value': 12},
                 {'label': '24', 'value': 24},
                 {'label': '36', 'value': 36}],
        value=12,
    ),
    # figure

    dcc.Graph(id='heatmap-subplots')
])

@app.callback(
    # input and output of the function decorated by @app.callback
    Output(component_id='heatmap-subplots', component_property='figure'),
    Input(component_id='standardized_index', component_property='value'),
    Input(component_id='agg_lvl_in_months', component_property='value'),
    Input(component_id='ensemble_member', component_property='value')
)
def drought_classes_heatmaps(si, nm, em):
    """
    Plot the fraction in 3 drought severity classes for 3 periods based on a given PPE member,
    drought index and aggregation level.
    :param si: drought index as used in variable names (spi or spei)
    :param nm: aggregation level in months (int)
    :param em: ensemble member of interest (int)
    :return: plotly figure object with data and layout
    """
    # settings:
    datadir = "data/"
    rows = 3
    columns = 3

    # assertions:
    assert type(si) == str
    assert type(nm) == int
    assert type(em) == int

    # debug
    verbose = True

    datapaths = {key: sorted(
        glob.glob(datadir + "{}d-pct_{}_rcp85_land-rcm_uk_12km_{:02d}_BCI3_b6110_m.nc".format(key, si, em)))
                 for key in ['m', 'v', 'x']}
    if verbose:
        print("datapaths: \n", datapaths)

    dsdict = {k: xr.open_mfdataset(datapaths[k], combine='by_coords',
                                   preprocess=lambda ds: ds.expand_dims("ensemble_member"))
              for k in datapaths.keys()}
    if verbose:
        print("Data loaded")
    fig = make_subplots(rows=rows, cols=columns,
                        column_titles=[f"{p[0]}-{p[1]}" for p in np.array([dsdict['x'].timestart.dt.year.values,
                                                                           dsdict['x'].timestop.dt.year.values]).T],
                        row_titles=[f"Moderately dry", # (-1>{si}>=-1.5)
                                    f"Very dry", #  (-1.5>{si}>-2)
                                    f"Extremely dry"], #  (-2>{si})
                        x_title="Period", y_title="Drought severity class")

    for i, key in enumerate(datapaths.keys()):
        for t in range(3):
            data = dsdict[key][f"{key}-pct_{si}_{nm}"].isel(time=t, ensemble_member=0)
            fig.add_trace(
                go.Heatmap(z=data.values, coloraxis="coloraxis"),
                row=i+1, col=t+1 # indexing starts at 1 for some bizarre reason
            )
    fig.update_layout(coloraxis={'colorscale': 'Oranges'})
    for i in range(1, (rows * columns) + 1):
        fig['layout'][f'yaxis{i}']['scaleanchor'] = f'x{i}'
    fig.update_xaxes(showticklabels=False)
    if verbose:
        print("Finished figure")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
