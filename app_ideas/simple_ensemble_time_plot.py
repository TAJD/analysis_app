"""Dash application to analyse routing results contained in text files.

Thomas Dickson
thomas.dickson@soton.ac.uk
15/03/2019
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


def list_to_slices(inputlist):
      """
      Convert a flatten list to a list of slices:
      test = [0,2,3,4,5,6,12,99,100,101,102,13,14,18,19,20,25]
      list_to_slices(test)
      -> [(0, 0), (2, 6), (12, 14), (18, 20), (25, 25), (99, 102)]
      """
      inputlist.sort()
      pointers = np.where(np.diff(inputlist) > 1)[0]
      pointers = zip(np.r_[0, pointers+1], np.r_[pointers, len(inputlist)-1])
      slices = [(inputlist[i], inputlist[j]) for i, j in pointers]
      return slices

dfs = load_data(data_folder_path)
dfs_processed = [return_df_stats(i, df) for i, df in enumerate(dfs)]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# plot ensembles based on checkbox selection


app.layout = html.Div([
    dcc.Graph(
        id='Ensemble weather routing',
        figure={
            'data': [
                go.Scatter(x=d.index,
                           y=d["mean"],
                           error_y=dict(
                            type='data',
                            array=d["std"],
                            visible=True
                        ),
                           mode='markers',
                           opacity=0.7,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                    },
                    name="Ensemble "+str(i)) for i, d in enumerate(dfs_processed)
            ],
            'layout': go.Layout(
                xaxis=dict(
                title ="Date",
                autorange=True,
                showgrid=True,
                zeroline=True,
                showline=True,
            ),
            yaxis=dict(
                title="Voyaging time (hrs)",
                autorange=True,
                showgrid=True,
                zeroline=True,
                showline=True,
            ),
                margin={'l': 100, 'b': 40, 't': 10, 'r': 100},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
