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
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
from plotly.subplots import make_subplots

import base64  # only needed to include images

#
external_stylesheets = [dbc.themes.SANDSTONE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server   # necessary for deployment on heroku with gunicorn

# images are more work than expected:
img_paths = dict(
    img_dash='img/Plotly_Dash_logo.png',
    img_uea="img/uea_pink_tlogo.png",
    img_aw="img/anglian_water_loveeverydrop_hor_tlogo.png",
    img_acws="img/anglian_centre_for_water_studies_tlogo.png",
    img_github="img/GitHub-Mark-64px.png")
encoded_images = {key: base64.b64encode(open(value, 'rb').read()) for key, value in img_paths.items()}
img_height_bottom = 90
img_height_top = 50

# text tab contents
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(  # <P>aragraph
                []
                ,
                className="card-text"),
            html.P([
                html.B("The figure on the right shows the fraction (%) of time in three simulated periods (columns) "
                       "that the (preprocessed) UKCP18 regional climate model (RCM) simulations are experiencing droughts of "
                       "three different categories (rows)"),
                " according to either the Standardized Precipitation Index (SPI; McKee et al., 1993) "
                "or the Standardized Precipitation Evaporation Index (SPEI; Vicente-Serrano et al., 2009)."
                " Standardized indices allow us to compare dryness across locations with different normal "
                "moisture levels, as dryness (or wetness) is expressed in how many "
                "standard deviations the current condition is removed from what is normal in a certain baseline period "
                "for a specific location. "
                "The SPI only considers atmospheric moisture supply (precipitation), while the SPEI "
                "also includes atmospheric moisture demand (potential evaporation).", html.Br(), html.Br(),
                "In general, all ensemble members agree on increased time spent in (extremely) dry conditions in England towards the future"
                " under the pessimistic RCP8.5 scenario, but there are strong regional differences."
                " When comparing SPI and SPEI, it is clear that a strong projected increase in "
                "evaporation leads to much stronger increases in time spent in (extreme) drought if we rely on SPEI. "
                "Later, an ensemble of hydrological (and water resource) models will help me find out what this means "
                "for the propagation of "
                "these droughts to water resources, and how SPI and SPEI compare to projected hydrological droughts. "
                "There are large differences between the UKCP18 RCM "
                "ensemble members, showing that the climate simulations are a large source of uncertainty for "
                "hydrological impact projections .", html.Br(),html.Br(),
                "Play around with the figure controls below and see for yourself!", html.Br(), html.Br(),
                " Please note that this analysis is "
                "in a very early stage and it is not unrealistic these results may undergo changes."]
                ,
                className="card-text")
        ]
    ),
    className="mt-3",
    color='light', inverse=False
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P([html.B("This week, ") ,"I automated the following steps from my current workflow where I was previously "
                   "using Ctrl+C Ctrl+V, and applied this on UEA\'s HPC system to generate the data visualized in the graph on the right:",
                   html.Ul([html.Li("Creating SLURM batch job submission script templates, with inputs specifying the job name, whether it is an array job and whether python is used"),
                            html.Li("Creating SLURM batch job scripts (using the above) for the same operation on different sets of files."),
                            html.Li("Creating the same set of figures for different sets of files.")]),
                   "These bash scripts can be found in this", html.A([" GitHub repository. "], href="https://github.com/nelerey/bash_utils", )
                    ], # TODO insert github link
                   className="card-text"),
            html.P(["Aside from this, for the creation of the data and figures shown and for writing this app,"
                   " many bash commands and structures learnt this week were very helpful to manipulate and transfer "
                    "files, such as ", html.B("for loops"), ", ",
                    html.B("seq"),", ", html.B("rsync"), ", ", html.B("tar"), ", ", html.B("tail"), "..."]
                   , className="card-text"),
            html.P([html.B("Later in my project, "), "I will make much more extensive use of bash scripting when "
                    "working with hydrological models. The bash scripting skills I learned this week (and will further develop)"
                    " will be extremely useful for the following (non-exhaustive!) list of tasks:",
                    html.Ul([
                        html.Li(["Generate input files for the different hydrological models based on different forcing"
                                 " datasets, for different catchments. "]),
                        html.Li(["Generate text files that define the structure of a hydrological model with the FUSE modular framework (Clark et al., 2008)"],),
                        html.Li(["Automatically calibrate the selected hydrological models for a number of catchments in East Anglia and retain a number of good parameter sets"]),
                        html.Li(["Automatically run the hydrological models with different parameter sets to obtain an ensemble of "
                                 "streamflow simulations for different catchments"]),
                        html.Li(["Connect different parts of this chain"]),
                    ]),
                    ],  # TODO describe future workflow and how I'll automnate the living shit out of it
                   className="card-text"),
            html.P([
                "Because of the size of the datasets and the computational demands of the operations involved with "
                "this work, most of my work is done on HPC systems. "
                "Generally, I develop code locally on small toy datasets on my laptop, check if it works, "
                "push it to Github, log onto the hpc, pull the changes from Github and submit a SLURM batch job (array) "
                "that runs the code on the larger, \"real\" datasets. "
                "When I need to make (more complicated) figures, the datasets containing the result of an analysis "
                "are transferred to my laptop where I make the figures. I started automating elements of this workflow "
                "this week, but there is room for improvement."
            ])
        ]
    ),
    className="mt-3",
    color='light', inverse=False
)


tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(["This interactive poster was made in Plotly Dash, with helpful tips & tricks from Victor Sonck.",
                   html.Br(),
                   "Theme: ", html.A("https://bootswatch.com/sandstone/.", href="https://bootswatch.com/sandstone/"), html.Br(),
                   "You can find this app on", html.A("GitHub.", href="https://github.com/nelerey/dash_app_advancedscriptingcourse")],
                   className="card-text"),
            html.H5("References:"),
            html.P(["McKee, T. B., Doesken, N. J., & Kleist, J. (1993). The relationship of drought frequency and duration to time scales. In Proceedings of the 8th Conference on Applied Climatology (Vol. 17, No. 22, pp. 179-183).", html.Br() ,
                   "Vicente-Serrano, S. M., Beguería, S., & López-Moreno, J. I. (2009). A multiscalar drought index sensitive to global warming: the standardized precipitation evapotranspiration index. Journal of climate, 23(7), 1696-1718.", html.Br() ,
                   "Clark, M. P., Slater, A. G., Rupp, D. E., Woods, R. A., Vrugt, J. A., Gupta, H. V., ... & Hay, L. E. (2008). Framework for Understanding Structural Errors (FUSE): A modular framework to diagnose differences between hydrological models. Water Resources Research, 44(12).",html.Br() ,
                   "Met Office Hadley Centre (2018): UKCP18 Regional Projections on a 12km grid over the UK for 1980-2080. Centre for Environmental Data Analysis, 14 February 2021. https://catalogue.ceda.ac.uk/uuid/589211abeb844070a95d061c8cc7f604",html.Br() ],
                   className="card-text")
        ]
    ),
    className="mt-3",
    color='light', inverse=False
)


input_panel = dbc.FormGroup(
    # select whether to show spi or spei, make spi default
    [dbc.Label('Drought index: '),
     dbc.RadioItems(id="standardized_index",
                    options=[
                        {'label': 'SPI', 'value': 'spi'},
                        {'label': 'SPEI', 'value': 'spei'}
                    ],
                    value='spi',
                    ),
     # select ensemble member to show
     dbc.Label('UKCP18 RCM PPE member:',
               ),
     dbc.Select(id="ensemble_member",
                options=[{'label': 'ensemble member 1 (STD)', 'value': 1}] +
                        [{'label': f'ensemble member {i}', 'value': i} for i in range(4, 14)] +
                        [{'label': f'ensemble member 15', 'value': 15}],
                value=1,
                ),
     # select aggregation level to show
     dbc.Label('Drought index aggregation level in months:',
               ),
     dbc.Select(id="agg_lvl_in_months",
                options=[{'label': '1', 'value': 1},
                         {'label': '3', 'value': 3},
                         {'label': '6', 'value': 6},
                         {'label': '12', 'value': 12},
                         {'label': '24', 'value': 24},
                         {'label': '36', 'value': 36}],
                value=12,
                )
     ])


project_info = dbc.Card(
    dbc.CardBody(
        [html.H5("Project summary"),
            html.P(["Extreme droughts can cause enormous ecological and economic damage, and are expected to "
                   "become more severe in some regions due to climate change. For water managers, it is "
                   "crucial to understand extreme droughts and how they are projected to change compared "
                   "to previous droughts, in order to plan for resilience to these events. "
                   "In this PhD project, which is funded on a 50/50 basis by the University of East Anglia and "
                   "the water company Anglian Water, I aim to increase our "
                   "understanding of future extreme droughts by answering the following",
                   html.B(" research questions: "),
                   html.Ol([
                       html.Li("How are properties (severity, frequency, extent and duration) of extreme droughts expected to change due to climate change?"),
                       html.Li("How do the hydrometeorological processes involved in drought propagation contribute to changes in drought severity, frequency, extent and duration? "),
                       html.Li("How is climate change expected to influence the impacts of extreme and severe droughts in (simple and more integrated) water resources systems? "),
                   ]),
                   "For this, I make use of the UKCP18 regional climate projections (Met Office, 2018),"
                   " thousands of years of simulated weather and an ensemble of hydrological "
                   "(and water resources) models."
                   ], className="card-text")]
    ),
    className="mt-3",
    color='primary', inverse=True
)


# Set up the app layout
app.layout = html.Div([
    html.Br(),



    # header with project explanation box
    dbc.Row(
        [dbc.Col(  # app title and subtitle (~ sci poster).
            [html.H1('SCRIPTING FOR DROUGHT RESILIENCE', className="display-3", style={"text-align": "left"}),
             html.H4(children='Nele Reyniers, University of East Anglia', style={"text-align": "left"})],
            width=10),
            dbc.Col([dbc.Row(html.Img(src='data:image/png;base64,{}'.format(encoded_images['img_dash'].decode()),
                                      style={'height': img_height_top*2, 'align': 'right'})),
                     dbc.Row(html.A([html.Img(src='data:image/png;base64,{}'.format(encoded_images['img_github'].decode()),
                                       style={'height': img_height_top, 'align': 'right'})],
                                    href="https://github.com/nelerey/dash_app_advancedscriptingcourse"))],
                    width=2),
        ]
    ),
    dbc.Row(dbc.Col(
              project_info
        )),
    html.Br(),
    # main body: graph and text
    dbc.Row([
        # draw some maps
        dbc.Col([
            dbc.Row(
                dbc.Tabs(
                    [
                        dbc.Tab([
                            tab1_content,
                            input_panel
                        ], label="Plot info"),
                        dbc.Tab(tab2_content, label="Automating my workflow"),
                        dbc.Tab(tab3_content, label="App info and references"),
                    ]
                )
            )
        ], width=6),
        dbc.Col(
            dcc.Graph(id='heatmap-subplots'), width=6,
        ),
    ]),dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_images['img_uea'].decode()),
                          style={'height': img_height_bottom})]),
        dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_images['img_acws'].decode()),
                          style={'height': img_height_bottom})]),
        dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_images['img_aw'].decode()),
                          style={'height': img_height_bottom})]),
        dbc.Col([], width=3),
    ],
    ),
    html.Br()
], style={"margin-left": 30, "margin-right": 30})

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
    em = int(em)
    nm = int(nm)

    # assertions:
    assert type(si) == str
    assert type(nm) == int
    assert type(em) == int

    # debug
    verbose = False

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
                        #shared_xaxes=True,
                        #shared_yaxes=True,
                        column_titles=[f"{p[0]}-{p[1]}" for p in np.array([dsdict['x'].timestart.dt.year.values,
                                                                           dsdict['x'].timestop.dt.year.values]).T],
                        row_titles=[f"Moderately dry",  # (-1>{si}>=-1.5)
                                    f"Very dry",  #  (-1.5>{si}>-2)
                                    f"Extremely dry"],  #  (-2>{si})
                        x_title="Period", y_title="Drought severity class",
                        horizontal_spacing=0.01, vertical_spacing=0.02)

    for i, key in enumerate(datapaths.keys()):
        for t in range(3):
            data = dsdict[key][f"{key}-pct_{si}_{nm}"].isel(time=t, ensemble_member=0)
            fig.add_trace(
                go.Heatmap(z=data.values, coloraxis="coloraxis"),
                row=i+1, col=t+1  # indexing starts at 1 for some bizarre reason
            )

            # fig.update_yaxes(scaleanchor='x', scaleratio=1, showticklabels=False)
    fig.update_layout(coloraxis={'colorscale': 'solar_r'})

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    for i in range(1, (rows * columns) + 1):
        # from the yaxis layout docs: " Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden"
        # sad
        fig['layout'][f'yaxis{i}']['scaleanchor'] = f'x{i}'
    fig['layout']['height'] = 700

    if verbose:
        print("Finished figure")

    return fig


if __name__ == '__main__':
    # this is not used in production
    app.run_server(debug=True)
