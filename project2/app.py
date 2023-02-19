from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
import json

# project import
import component_ids as ids


# ~~~ Global variables & data ~~~
with open("features.json", "r") as fin:
    features:dict[str, list[str]] = json.load(fin)
    
NUMERICAL = features["NUMERICAL"]
data = pd.read_csv("data/absenteeism_at_work_preprocessed.csv")
pca = PCA()

# ~~~ App ~~~
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Insert title here"

app.layout = (
    html.Div(className="main-div",
             children=[
                 html.H1("Absenteeism at Work", className="h1"),
                 html.H4("By: Eric Sclafani", className="h4"),
                 
             ])
)



if __name__ == "__main__":
    app.run_server(debug=True)