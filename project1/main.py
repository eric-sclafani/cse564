# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/preprocessed/absenteeism_at_work_preprocessed.csv")

# ~~~ APP ~~~
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Absenteeism at Work"

# ~~~ LAYOUT ~~~
app.layout = html.Div([
    html.H1("Absenteeism at Work", className="h1"),
    html.Hr(),
    html.H2("Select a variable from the dropdown menu"),
    html.Div(
        className="dropdown-variables",
        children=[
            dcc.Dropdown(
                id="dropdown",
                options=["month", "day_of_week"],
                value="month",
                clearable=False)]),
    html.Div(
        className="graph-div",
        children=[
            dcc.Graph(id="graph")])
    ])



# ~~~ CALLBACKS ~~~
@app.callback(Output("graph", "figure"),
              Input("dropdown", "value"))
def bar_chart(feature):
    fig = px.bar(df, x=feature, color=feature)
    fig.update_layout(transition_duration=500)
    return fig


    
if __name__ == '__main__':
    app.run_server(debug=True)