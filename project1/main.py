# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json
from typing import Union


# ~~~ GLOBAL VARIABLES ~~~
df = pd.read_csv("data/preprocessed/absenteeism_at_work_preprocessed.csv")
df["Absence reason"] = df["Absence reason"].astype("category")

CATEGORICAL = [
    "Month",
    "Absence reason", 
    "Day", 
    "Season", 
    "Education level", 
    "Disease"
    ]

NUMERICAL = [
    "Transportation expense",
    "Distance to work",
    "Service time",
    "Age",
    "Avg work load per day",
    "Number of children",
    "Pets",
    "Weight",
    "Height",
    "Body mass index",
    "Time absent"
    ]

# ~~~ HELPER FUNCTIONS ~~~

def get_orientation(option:str) -> str:
    """Gets barchart orientation argument from radiobutton string value"""
    return "h" if option == "Horizontal" else "v"

def make_bar_chart(orientation:str, feature:str) -> px.bar:
    """Creates a bar chart according to given arguments"""
    title = f"Number of absences per {feature.lower()}" #NOTE: add better title string formatting and axes 
    count = {"count": "Number of absences"}
    
    if orientation == "v":
        fig = px.bar(df, 
                     x=feature, 
                     color=feature, 
                     title=title,
                     orientation=orientation,
                     labels=count,)
        
    elif orientation == "h":
        fig = px.bar(df,
                     y=feature, 
                     color=feature, 
                     title=title,
                     orientation=orientation,
                     labels=count)
    return fig   

def make_histogram(orientation:str, feature:str) -> px.histogram:
    """Creates a histogramn according to given parameters"""
    bin_size = 10
    title = f"Distribution of {feature.lower()}" 
    new_labels = {"count": "Number of absences",
                  "Service time": "Service time (years)",
                  "Height": "Height (cm)",
                  "Weight": "Weight (kg)",
                  "Time absent": "Time absent (hrs)",
                  "Distance to work": "Distance to work (km)",
                  "Transportation expense": "Transportation expense (Brazilian Real)"}
    
    if orientation == "v":
        fig = px.histogram(df, 
                     x=feature,  
                     title=title,
                     orientation=orientation,
                     labels=new_labels,
                     nbins=bin_size)
        
    elif orientation == "h":
        fig = px.histogram(df,
                     y=feature, 
                     title=title,
                     orientation=orientation,
                     labels=new_labels,
                     nbins=bin_size)
    return fig
        
    

# ~~~ APP ~~~
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Absenteeism at Work"

# ~~~ LAYOUT ~~~
app.layout = html.Div(children=[
    html.H1("Absenteeism at Work", className="h1"),
    html.Hr(),
    html.H2("Select a feature"), #! style this
    
    html.Div(
        className="dropdown-variables",
        children=[
            dcc.Dropdown(
                id="feature-dropdown",
                options=CATEGORICAL + NUMERICAL,
                value="Month",
                clearable=False)]),
    
    html.Div(
        className="graph-div",
        children=[
            dcc.RadioItems(["Vertical", "Horizontal"],
                           "Vertical",
                           labelStyle={'display': 'block'}, # forces vertical alignment
                           id="orientation"),
            
            dcc.Graph(id="tab1-graph")])
    ])



# ~~~ CALLBACKS ~~~
@app.callback(Output("tab1-graph", "figure"),
              Input("feature-dropdown", "value"),
              Input("orientation", "value"))
def tab1_graph(feature, orientation) -> Union[px.bar, px.histogram]:
    
    orientation = get_orientation(orientation)
    
    if feature in CATEGORICAL:
        fig = make_bar_chart(orientation, feature)
    elif feature in NUMERICAL:
        fig = make_histogram(orientation, feature)
        
    fig.update_layout(transition_duration=500, title_x=.5)
    fig.update_traces(dict(marker_line_width=0))
    
    return fig


    


    
if __name__ == '__main__':
    app.run_server(debug=True)