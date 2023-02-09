# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px

# ~~~ DATA AND HELPER FUNCTIONS ~~~

df = pd.read_csv("data/preprocessed/absenteeism_at_work_preprocessed.csv")

def get_orientation(option:str) -> str:
    """Gets barchart orientation argument from radiobutton option string"""
    return "h" if option == "Horizontal" else "v"

def get_bar_chart(orientation:str, feature:str) -> px.bar:
    
    title = f"Count of {feature}"
    
    if orientation == "v":
        fig = px.bar(df, x=feature, color=feature, title=title, orientation=orientation)
    else:
        fig = px.bar(df, y=feature, color=feature, title=title, orientation=orientation)
    return fig
    

# ~~~ APP ~~~
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Absenteeism at Work"

# ~~~ LAYOUT ~~~
app.layout = html.Div(children=[
    html.H1("Absenteeism at Work", className="h1"),
    html.Hr(),
    html.H2("Select a variable"),
    html.Div(
        className="dropdown-variables",
        children=[
            dcc.Dropdown(
                id="feature-dropdown",
                options=["month", "day_of_week"],
                value="month",
                clearable=False)]),
    
    html.Div(
        className="graph-div",
        children=[
            dcc.RadioItems(["Vertical", "Horizontal"], "Vertical",labelStyle={'display': 'block'}, id="orientation"),
            dcc.Graph(id="barchart")])
    ])



# ~~~ CALLBACKS ~~~
@app.callback(Output("barchart", "figure"),
              Input("feature-dropdown", "value"),
              Input("orientation", "value"))
def bar_chart(feature, orientation):
    
    orientation = get_orientation(orientation)
    fig = get_bar_chart(orientation, feature)
    fig.update_layout(transition_duration=500, title_x=.5)
    return fig


    


    
if __name__ == '__main__':
    app.run_server(debug=True)