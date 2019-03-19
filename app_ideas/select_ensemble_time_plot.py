"""Dash application to plot routes from .h5 files.

Thomas Dickson
thomas.dickson@soton.ac.uk
16/03/2019
"""

from mpl_toolkits.basemap import Basemap
from os import listdir
import datetime, re, dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from os.path import isfile, join
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output

data_folder_path = "/home/thomas/iridis/sail_route_old/development/polynesian/ensemble_testing/sample_folder/"


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
    dfs = [pd.read_csv(data_path+file, index_col=0) for file in onlyfiles]
    return dfs


def return_df_stats(i, df):
    """Return a dataframe of the mean and std of a dataframe"""
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    df = pd.concat([mean, std], axis=1)
    df.columns = ["mean", "std"]
    return df


dfs = load_data(data_folder_path)
dfs_processed = [return_df_stats(i, df) for i, df in enumerate(dfs)]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### Ensemble voyaging time plotting tool

A simple tool for plotting voyaging time as a function of ensemble and start date.
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text),
    dcc.Graph(id='ensemble-voyaging-time-plot'),
    dcc.Dropdown(
        id='ensemble-selection',
        options=[{'label': "Ensemble "+str(i), 'value':str(i)} for i in range(0, len(dfs))],
        value=[i for i in range(0, len(dfs))],
        multi=True
    )
])


@app.callback(
    Output('ensemble-voyaging-time-plot', 'figure'),
    [Input('ensemble-selection', 'value')])
def update_figure(ensembles):
    ensembles = list(map(int, ensembles))
    filtered_df = [dfs_processed[i] for i in ensembles]
    traces = []
    for i, df in enumerate(filtered_df): # re-write using enumerate
        traces.append(go.Scatter(
            x=df.index,
            y=df["mean"],
            error_y=dict(type='data', array=df["std"], visible=True),
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name="Ensemble "+str(i))
        )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Voyaging time (hrs)'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

# ensemble weather routing analysis app
# 0. Would be cool to run the app and to interactively specify the dataset before the server runs.
# 1. load the dataframes
# 2. calculate the average voyaging time for each start time and ensemble scenario
# 3. plot the voyaging time for all ensemble scenarios


if __name__ == '__main__':
    app.run_server(debug=True)