from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
import json

# project import
import component_ids as ids

with open("features.json", "r") as fin:
    features:dict[str, list[str]] = json.load(fin)

data = pd.read_csv("data/absenteeism_at_work.csv")

app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Insert title here"

app.layout = ()






if __name__ == "__main__":
    app.run_server(debug=True)