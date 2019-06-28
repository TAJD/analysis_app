import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
try:
    from itertools import izip# Python 2
except ImportError:
    izip = zip# Python 3

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/globe_contours.csv')
df.head()

contours = []

scl = ['rgb(213,62,79)', 'rgb(244,109,67)', 'rgb(253,174,97)', \
    'rgb(254,224,139)', 'rgb(255,255,191)', 'rgb(230,245,152)', \
    'rgb(171,221,164)', 'rgb(102,194,165)', 'rgb(50,136,189)'
]

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

i = 0
for lat, lon in pairwise(df.columns):
    contours.append(go.Scattergeo(
        lon = df[lon],
        lat = df[lat],
        mode = 'lines',
        line = go.scattergeo.Line(
            width = 2,
            color = scl[i]
        )))
    i = 0 if i + 1 >= len(df.columns) / 4 else i + 1

layout = go.Layout(
    title = go.layout.Title(
        text = 'Contour lines over globe<br>(Click and drag to rotate)'
    ),
    showlegend = False,
    geo = go.layout.Geo(
        showland = True,
        showlakes = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.5,
        landcolor = 'rgb(230, 145, 56)',
        lakecolor = 'rgb(0, 255, 255)',
        oceancolor = 'rgb(0, 255, 255)',
        projection = go.layout.geo.Projection(
            type = 'orthographic',
            rotation = go.layout.geo.projection.Rotation(
                lon = -100,
                lat = 40,
                roll = 0
            )
        ),
        lonaxis = go.layout.geo.Lonaxis(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        ),
        lataxis = go.layout.geo.Lataxis(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        )
    )
)

fig = go.Figure(data = contours, layout = layout)
py.iplot(fig, filename = 'd3-globe')