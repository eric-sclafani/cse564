# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px

# ~~~ DATA HANDLING ~~~
df = pd.read_csv("data/bike_sharing_daily.csv")
df.rename(columns={"instant":"id",
                    "dteday":"datetime",
                    "yr":"year",
                    "mnth":"month",
                    "holiday":"is_holiday",
                    "workingday":"is_workday",
                    "cnt": "total_count",
                    "weathersit":"weather_type"},
          inplace=True)
df["datetime"] = pd.to_datetime(df["datetime"])

print(df.info())






# ~~~ APP ~~~
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Daily bike sharing"



# ~~~ LAYOUT ~~~
app.layout = html.Div([
    html.H1("Daily bike sharing"),
    html.Hr(),
    html.H2("Select a variable from the dropdown menu"),
    dcc.Dropdown(
        id="dropdown",
        options=["1", "2", "3", "4"],
        value="1",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])



# ~~~ CALLBACKS ~~~
@app.callback(Output("graph", "figure"),
              Input("dropdown", "value"))
def update_bar_chart(day):
    
    df = px.data.tips() # replace with your own data source
    filtered_df = df[df['day'] == day]
    fig = px.bar(filtered_df, x="sex", y="total_bill", 
                 color="smoker", barmode="group")
    return fig


    
# if __name__ == '__main__':
#     app.run_server(debug=True)