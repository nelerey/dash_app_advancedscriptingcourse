"""
Make maps of my data in plotly.
This script is preparation to make a dash app
"""
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.colors import sequential as cmseq
import xarray as xr
import numpy as np
import glob
import pathlib
import matplotlib.pyplot as plt


# figure
def drought_classes_heatmaps(si, nm, em):
    """
    Plot the fraction in 3 drought severity classes for 3 periods based on a given PPE member,
    drought index and aggregation level.
    :param si: drought index as used in variable names (spi or spei)
    :param nm: aggregation level in months (int)
    :param em: ensemble member of interest (int)
    :return: plotly figure object with data and layout
    """
    datadir = "./data/"

    datapaths = {key: sorted(
        glob.glob(datadir + "{}d-pct_{}_rcp85_land-rcm_uk_12km_{:02d}_BCI3_b6110_mgev.nc".format(key, si, em)))
                 for key in ['m', 'v', 'x']}

    dsdict = {k: xr.open_mfdataset(datapaths[k], combine='by_coords',
                                   preprocess=lambda ds: ds.expand_dims("ensemble_member"))
              for k in datapaths.keys()}
    fig = make_subplots(rows=3, cols=3,
                        column_titles=[f"{p[0]}-{p[1]}" for p in np.array([dsdict['x'].timestart.dt.year.values,
                                                                           dsdict['x'].timestop.dt.year.values]).T],
                        row_titles=[f"Moderately dry (-1>{si}>=-1.5)",
                                    f"Very dry (-1.5>{si}>-2)",
                                    f"Extremely dry (-2>{si})"],
                        x_title="Period", y_title="Drought severity class")

    for i, key in enumerate(datapaths.keys()):
        for t in range(3):
            data = dsdict[key][f"{key}-pct_{si}_{nm}"].isel(time=t, ensemble_member=0)
            fig.add_trace(
                go.Heatmap(z=data.values, coloraxis="coloraxis"),
                row=i+1, col=t+1 # indexing starts at 1 for some bizarre reason
            )
    fig.update_layout(coloraxis={'colorscale': 'Oranges'})
    fig.update_yaxes(scaleanchor='x', scaleratio=1, showticklabels=False)
    fig.update_xaxes(showticklabels=False)
    return fig

# test the function
em = 1
si = 'spei'
nm = 12
funfig = drought_classes_heatmaps('spei', 12, 1)
funfig.show()
