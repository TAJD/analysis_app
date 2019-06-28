import base64
import datetime
import io, h5py, numpy as np, pandas as pd

from textwrap import dedent as d

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import plotly.plotly as py
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


def return_data_arrays(h5_file):
    et_results = np.array(h5_file['et_results'])
    journey_times = np.array(h5_file['journey_times'])
    unix_times = np.array(h5_file['start_times'])
    start_times = np.array([datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%SZ') for t in unix_times])
    start_times = np.array([datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ') for t in start_times])
    x_locations = np.array(h5_file['x_locations'])
    y_locations = np.array(h5_file['y_locations'])
    x_results = np.array(h5_file['x_results'])
    y_results = np.array(h5_file['y_results'])
    journey_times[journey_times==0] = np.nan

    df = pd.DataFrame({'start times':start_times,'journey times':journey_times[1, :]}) # include all j
    print(x_results.shape)
    return df


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        h5_file = h5py.File(io.BytesIO(decoded), 'r')
        df = return_data_arrays(h5_file)

        graph = dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': df['start times'], 'y': df['journey times'], 'customdata': df.index, 'type': 'scatter', 'name': filename,'mode': 'markers', 'marker': {'size': 12}},
                ],
                'layout': {
                    'title': filename,
                    'clickmode': 'event+select'
                }
            }
        )
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([graph])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# @app.callback(
#     Output('click-data', 'children'),
#     [Input('basic-interactions', 'clickData')])
# def display_click_data(clickData):
#     print(clickData)
#     return json.dumps(clickData, indent=2)


# @app.callback(
#     Output('hover-data', 'children'),
#     [Input('basic-interactions', 'hoverData')])
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True)