#!/usr/bin/env python3

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd 

# project imports
import ids
import components



# ~~~ Global variables ~~~



# ~~~ Helper functions ~~~





# ~~~ App ~~~
    
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Insert title here"

app.layout = html.Div(children=[
    
                html.Div(className="main-div",
                        children=[
                            html.H1("Absenteeism at Work", className="h1"),
                            html.H4("By: Eric Sclafani", className="h4")]),
    
                html.Div(className="graph-div",
                        children=[
                            dcc.Graph()]),
])

# ~~~ Callbacks ~~~




if __name__ == "__main__":
   app.run_server(debug=True)