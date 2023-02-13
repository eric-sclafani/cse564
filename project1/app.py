# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px
import json
from typing import Union


# ~~~ GLOBAL VARIABLES ~~~
df = pd.read_csv("data/preprocessed/absenteeism_at_work_preprocessed.csv")
df["Absence reason"] = df["Absence reason"].astype("category")

with open("features.json", "r") as fin:
    features:dict[str, list[str]] = json.load(fin)
    
CATEGORICAL = features["CATEGORICAL"]
NUMERICAL = features["NUMERICAL"]
NEW_LABELS = {
        "Service time": "Service time (years)",
        "Height": "Height (cm)",
        "Weight": "Weight (kg)",
        "Time absent": "Time absent (hrs)",
        "Distance to work": "Distance to work (km)",
        "Transportation expense": "Transportation expense (Brazilian Real)"
        }


# ~~~ HELPER FUNCTIONS ~~~

def get_orientation(option:str) -> str:
    """Gets orientation argument for barchart/histogram from radiobutton string value"""
    return "h" if option == "Horizontal" else "v"

def make_bar_chart(orientation:str, feature:str):
    """Creates a bar chart according to given arguments"""
    title = f"Number of absences per {feature.lower()}"
    rename_count = {"count":"Number of absences"}
    if orientation == "v":
        fig = px.bar(df, 
                     x=feature, 
                     color=feature, 
                     title=title,
                     orientation=orientation,
                     labels=rename_count)
        
    elif orientation == "h":
        fig = px.bar(df,
                     y=feature, 
                     color=feature, 
                     title=title,
                     orientation=orientation,
                     labels=rename_count)
    return fig   

def make_histogram(orientation:str, feature:str):
    """Creates a histogram according to given parameters"""
    bin_size = 10
    title = f"Distribution of {feature.lower()}" 
    
    if orientation == "v":
        fig = px.histogram(df, 
                     x=feature,  
                     title=title,
                     orientation=orientation,
                     labels=NEW_LABELS,
                     nbins=bin_size)
        fig.update_layout(yaxis_title="Number of absences")
        
    elif orientation == "h":
        fig = px.histogram(df,
                     y=feature, 
                     title=title,
                     orientation=orientation,
                     labels=NEW_LABELS,
                     nbins=bin_size)
        fig.update_layout(xaxis_title="Number of absences")
    return fig

def make_scatter_plot(feature_x:str, feature_y:str):
    """Creates a scatterplot given x and y"""
    fig = px.scatter(df, x=feature_x, y=feature_y, labels=NEW_LABELS)
    return fig
    
    
        
# ~~~ APP ~~~

app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Absenteeism at Work"


# ~~~ LAYOUT ~~~

app.layout = html.Div(children=[
    html.Hr(),
    html.H1("Absenteeism at Work", className="h1"),
    html.H4("By: Eric Sclafani", className="h4"),
    html.Hr(),
    dcc.Tabs(children=[
        dcc.Tab(label="Charts", className="tab1", children=[
            html.Div(children=[
                html.H2("Select a feature", className="h2"), #! style this
                
                #! TAB1 DROPDOWN MENU
                html.Div(
                    className="dropdown-variables",
                    children=[  
                        dcc.Dropdown(
                            id="feature-dropdown",
                            options=CATEGORICAL + NUMERICAL,
                            value="Month",
                            clearable=False,
                            className="dropdown-text")]),
                
                #! TAB1 RADIOBUTTON & CHART
                html.Div(
                    className="graph-div",
                    children=[         
                        dcc.RadioItems(
                            options=["Vertical", "Horizontal"],
                            value="Vertical",
                            id="orientation",
                            className="tab1-radiobutton"),

                        dcc.Graph(id="tab1-graph")])],
                     style={"text-align": "center"})]),
        
        dcc.Tab(label="Scatterplot", className="tab2",children=[
            
            #! TAB 2 X-AXIS RADIOBUTTON + SCATTERPLOT + Y-AXIS RADIOBUTTON
            html.Div(children=[
                html.Div(children=[
                    html.H2("Choose x axis", className="h2"),
                    dcc.RadioItems(
                            options=CATEGORICAL+NUMERICAL,
                            value="Age",
                            labelStyle={'display': 'block'},
                            id="x-axis-radio",
                            className="tab2-radiobutton")],
                        style={'display': 'inline-block', "text-align": "left"}),
                
                html.Div(children=[
                    dcc.Graph(
                            id="tab2-graph")],
                        style={'display': 'inline-block',}),
                
                html.Div(children=[
                    html.H2("Choose y axis", className="h2"),
                    dcc.RadioItems(
                            options=CATEGORICAL+NUMERICAL,
                            value="Time absent",
                            labelStyle={'display': 'block'},
                            id="y-axis-radio",
                            className="tab2-radiobutton")],
                        style={'display': 'inline-block', "text-align": "right"})],
                     style={"text-align": "center"})])
    ]),
])


# ~~~ CALLBACKS ~~~

@app.callback(Output("tab1-graph", "figure"),
              Input("feature-dropdown", "value"),
              Input("orientation", "value"))
def tab1_graph(feature, orientation) -> Union[px.bar, px.histogram]:
    """This callback generates a bar chart or histogram depending on the event chosen"""
    orientation = get_orientation(orientation)
    
    if feature in CATEGORICAL:
        fig = make_bar_chart(orientation, feature)
    elif feature in NUMERICAL:
        fig = make_histogram(orientation, feature)
        
    fig.update_layout(transition_duration=500, title_x=0.5)
    fig.update_traces(dict(marker_line_width=0))
    
    return fig


@app.callback(Output("tab2-graph", "figure"),
              Input("x-axis-radio", "value"),
              Input("y-axis-radio", "value"))
def tab2_graph(feature_x, feature_y):
    """This callback generates a scatterplot when given x and y features"""
    fig = make_scatter_plot(feature_x, feature_y)
    fig.update_layout(title=f"{feature_x} vs. {feature_y}", title_x=0.5, transition_duration=500)
    return fig


    
if __name__ == '__main__':
    app.run_server(debug=True)