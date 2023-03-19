from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components import themes
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import pandas as pd 
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # suppress annoying kmeans future warning

# project imports
import tabs

# ~~~ APP ~~~
app = Dash(__name__, external_stylesheets=[themes.LITERA])
app.title = "PAN 2022 Features"


app.layout = html.Div([
    html.Div(className="main-div",
             children=[
                 html.H1("PAN 2022 Features", className="h1"),
                 html.H4("By: Eric Sclafani", className="h4"),
                 html.Hr()]),
    
    html.Div(className="tabs-div",
             children=[
                dbc.Tabs([
                    tabs.mds_tab,
                    tabs.pcp_tab])])
    ]
                      )








if __name__ == "__main__":
    app.run_server(debug=True)