#!/usr/bin/env python3

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import CERULEAN
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # suppress annoying kmeans future warning

# ~~~ Global variables ~~~
df = pd.read_csv("data/pan22_features.csv")
numericals_df = df.drop(columns=["author_id", "discourse_type"]).values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(numericals_df)
Y = df["author_id"].values

pca = PCA(n_components=7) # n_components determined through experimentation in testing.ipynb
X_reduced = pca.fit_transform(X_scaled)


# ~~~ Helper functions ~~~

def make_scree_plot(n_to_show:int) -> go.Figure:
    """
    Creates a scree plot (scatter plot w/ line + bar chart) given n # of principal components to show
    :param n_to_show: number of principal components to show. Received from scree_plot_graph callback
    :rerurns: plotly figure representing a scree plot
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(1,8))[0:n_to_show],
            y=pca.explained_variance_ratio_.cumsum()[0:n_to_show],
            name="Cumulative explained variance",
            hoverlabel={"namelength":-1}))
    fig.add_trace(
        go.Bar(
            x=list(range(1,8))[0:n_to_show], 
            y=pca.explained_variance_ratio_[0:n_to_show],
            name="PC"))
                 
    fig.update_xaxes(type="category")
    fig.update_layout(
        title="Explained variance per principle component",
        title_x = 0.5,
        xaxis_title="Principal Component", 
        yaxis_title="% Explained variance",
        transition_duration=500)
    return fig
    
    
def make_k_plot() -> go.Figure:
    """
    Creates a visualization of the objective function in K means
    :returns: plotly lineplot
    """
    within_cluster_sum_squares = []
    candidate_k_values = range(1,16)
    for k in candidate_k_values:
        model = KMeans(n_clusters=k, random_state=1)
        model.fit(X_reduced)
        within_cluster_sum_squares.append(model.inertia_)

    kmeans_df = pd.DataFrame({
        "K":candidate_k_values,
        "Within Cluster Sum of Squares (WCSS)":within_cluster_sum_squares})
    
    fig = px.line(kmeans_df, 
            x="K", 
            y="Within Cluster Sum of Squares (WCSS)", 
            markers=True,
            title="WCSS Error per K cluster")
    fig.update_layout(title_x=0.5)
    
    return fig


def make_biplot():
    
    model = KMeans(n_clusters=3, random_state=1)
    model.fit(X_reduced)
    
    
    


# ~~~ App ~~~
    
app = Dash(__name__, external_stylesheets=[CERULEAN])
app.title = "PAN 2022 Features"

app.layout = html.Div(children=[
    
    html.Div(className="main-div",
             children=[
                 html.H1("PAN 2022 Features", className="h1"),
                 html.H4("By: Eric Sclafani", className="h4")
                 ]),
    
    html.Div(className="scree-plot-div",
             children=[
                 dcc.Graph(id="scree-plot", className="scree-plot"),
                 html.P("Select number of components"),
                 dcc.Slider(id="scree-slider", 
                            min=2, 
                            max=7, 
                            step=1, 
                            value=2)]),
    
    html.Div(className="k-function-plot-div",
             children=[
                dcc.Graph(figure=make_k_plot(), id="k-function-plot")
             ])
])

# ~~~ Callbacks ~~~

@app.callback(Output("scree-plot", "figure"),
              Input("scree-slider", "value"))
def scree_plot_graph(n_to_show:int):
    fig = make_scree_plot(n_to_show)
    return fig


if __name__ == "__main__":
   app.run_server(debug=True)