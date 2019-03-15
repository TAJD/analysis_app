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


dfs = load_data(data_folder_path)


# dash app implementation

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



# create a dataframe containing the mean and standard deviation for each data for each ensemble


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div(children=[
#     html.H4(children='Ensemble weather scenario data'),
#     generate_table(dfs[0])
# ])
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/' +
#     '5d1ea79569ed194d432e56108a04d188/raw/' +
#     'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#     'gdp-life-exp-2007.csv')



app.layout = html.Div([
    dcc.Graph(
        id='Ensemble weather routing',
        figure={
            'data': [
                go.Scatter(x=d.index,
                           y=d.values,
                           mode='markers',
                           opacity=0.7,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                    },
                    name="Ensemble "+str(i)) for i, d in enumerate(dfs)
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


# ensemble weather routing analysis app
# 0. Would be cool to run the app and to interactively specify the dataset before the server runs.
# 1. load the dataframes
# 2. calculate the average voyaging time for each start time and ensemble scenario
# 3. plot the voyaging time for all ensemble scenarios


if __name__ == '__main__':
    app.run_server(debug=True)
