#!/usr/bin/env python3

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import CERULEAN
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd 

# ~~~ Global variables ~~~
df = pd.read_csv("data/pan22_features.csv")
numericals_df = df.drop(columns=["author_id", "discourse_type"]).values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(numericals_df)
Y = df["author_id"].values

pca = PCA(n_components=7) # n_components determined through experimentation in testing.ipynb
X_reduced = pca.fit_transform(X_scaled)


# ~~~ Helper functions ~~~

def make_scree_plot(n_to_show:int):
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=list(range(1,8))[0:n_to_show],
            y=np.cumsum(pca.explained_variance_[0:n_to_show]),
            name="Cumulative explained variance"))
    fig.add_trace(
        go.Bar(
            x=list(range(1,8))[0:n_to_show], 
            y=pca.explained_variance_[0:n_to_show],
            name="PC"))
                 
    fig.update_xaxes(type="category")
    fig.update_layout(
        title="Explained variance per principle component",
        title_x = 0.5,
        xaxis_title="Principal Component", 
        yaxis_title="% Explained variance")
    return fig
    



# ~~~ App ~~~
    
app = Dash(__name__, external_stylesheets=[CERULEAN])
app.title = "PAN 2022 Features"

app.layout = html.Div(children=[
    
    html.Div(className="main-div",
             children=[
                 html.H1("PAN 2022 Features", className="h1"),
                 html.H4("By: Eric Sclafani", className="h4")
                 ]),
    
    html.Div(className="graph-div",
             children=[
                 dcc.Graph(id="scree-plot"),
                 html.P("Select number of components"),
                 dcc.Slider(id="scree-slider", 
                            min=2, 
                            max=7, 
                            step=1, 
                            value=2,)
                 ]),
])

# ~~~ Callbacks ~~~

@app.callback(Output("scree-plot", "figure"),
              Input("scree-slider", "value"))
def scree_plot_graph(n_to_show:int):
    
    fig = make_scree_plot(n_to_show)
    
    return fig


if __name__ == "__main__":
   app.run_server(debug=True)