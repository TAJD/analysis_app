"""Dash application to plot routes from .h5 files.

Thomas Dickson
thomas.dickson@soton.ac.uk
16/03/2019
"""

from mpl_toolkits.basemap import Basemap
from os import listdir
import re, dash, h5py
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from os.path import isfile, join
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output
from datetime import datetime

data_path = "/home/thomas/iridis/sail_route_old/development/polynesian/ensemble_testing/trial_results/"


def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_nicely(l):
    return sorted(l, key=alphanum_key)


def load_data(data_path):
    """Load each txt file in a specified directory as a dataframe."""
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    sort_nicely(onlyfiles)
    files = [h5py.File(data_path+file, 'r') for file in onlyfiles]
    return files


def return_data_arrays(h5_file):
    et_results = np.ma.array(h5_file['et_results'])
    journey_times = np.ma.array(h5_file['journey_times'])
    unix_times = np.array(h5_file['start_times'])
    start_times = np.array([datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%SZ') for t in unix_times])
    x_locations = np.array(h5_file['x_locations'])
    y_locations = np.array(h5_file['y_locations'])
    x_results = np.ma.array(h5_file['x_results'])
    y_results = np.ma.array(h5_file['y_results'])
    journey_times[journey_times==0] = np.nan
    return et_results, start_times, journey_times, x_results, y_results, x_locations, y_locations


loaded_h5 = load_data(data_path)
et_results, start_times, journey_times, x_results, y_results, x_locations, y_locations = return_data_arrays(loaded_h5[0])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### Plot voyages

Tool to plot voyaging times and routes.
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text),
    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': start_times,
                    'y': journey_times,
                    'name': 'Voyaging time',
                    'mode': 'markers',
                    'marker': {'size': 12}
                },
            ],
            'layout': {
                'clickmode': 'event+select'
            }
        }
    ),
    # dcc.Dropdown(
    #     id='ensemble-selection',
    #     options=[{'label': "Ensemble "+str(i), 'value':str(i)} for i in range(0, len(dfs))],
    #     value=[i for i in range(0, len(dfs))],
    #     multi=True
    # )
])


# @app.callback(
#     Output('ensemble-voyaging-time-plot', 'figure'),
#     [Input('ensemble-selection', 'value')])
# def update_figure(ensembles):
#     ensembles = list(map(int, ensembles))
#     filtered_df = [dfs_processed[i] for i in ensembles]
#     traces = []
#     for i, df in enumerate(filtered_df): # re-write using enumerate
#         traces.append(go.Scatter(
#             x=df.index,
#             y=df["mean"],
#             error_y=dict(type='data', array=df["std"], visible=True),
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name="Ensemble "+str(i))
#         )

#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis={'title': 'Date'},
#             yaxis={'title': 'Voyaging time (hrs)'},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest'
#         )
#     }


if __name__ == '__main__':
    app.run_server(debug=True)