#!/usr/bin/env python3

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import CERULEAN
import dash_bootstrap_components as dbc
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

def make_scree_plot(n_to_highlight:int) -> go.Figure:
    """
    Creates a scree plot (scatter plot w/ line + bar chart) given n # of principal components to show
    :param n_to_show: number of principal components to show. Received from scree_plot_graph callback
    :rerurns: plotly figure representing a scree plot
    """
    fig = go.Figure()
    
    bar_colors = ["gray"] * 7
    bar_colors[n_to_highlight-1] = "red"
    
    fig.add_trace(
        go.Scatter(
            x=list(range(1,8)),
            y=pca.explained_variance_ratio_.cumsum(),
            name="Cumulative explained variance",
            hoverlabel={"namelength":-1}))
    fig.add_trace(
        go.Bar(
            x=list(range(1,8)), 
            y=pca.explained_variance_ratio_,
            name="PC",
            marker_color = bar_colors))
                 
    fig.update_xaxes(type="category")
    fig.update_layout(
        title="Explained variance per principle component",
        title_x = 0.25,
        xaxis_title="Principal Component", 
        yaxis_title="% Explained variance",
        transition_duration=500)
    return fig
    
    
def make_k_plot() -> go.Figure:
    """Creates a visualization of the objective function in K means"""
    sum_squares = []
    candidate_k_values = list(range(1,16))
    for k in candidate_k_values:
        model = KMeans(n_clusters=k, random_state=1)
        model.fit(X_reduced)
        sum_squares.append(model.inertia_)

    kmeans_df = pd.DataFrame({
        "K":candidate_k_values,
        "Sum of squares":sum_squares})
    
    fig = go.Figure()
    fig.add_trace(go.Line(
        kmeans_df, 
        x="K", 
        y="Sum of squares", 
        markers=True,
        title="Sum of Squares Error per K cluster"))
    
    fig.update_layout(title_x=0.5)
    
    return fig


def make_biplot() -> go.Figure:
    """Creates a biplot using the first two principal components"""
    model = KMeans(n_clusters=4, random_state=1)
    model.fit(X_reduced)

    pca_data_df = pd.DataFrame(X_reduced).rename(columns={0:"PC1", 1:"PC2", 2:"PC3", 3:"PC4", 4:"PC5", 5:"PC6", 6:"PC7"})
    kmeans_cluster_labels = pd.DataFrame({"K Cluster":model.labels_})

    kmeans_pca_df = pd.concat([df, pca_data_df, kmeans_cluster_labels], axis=1)
    fig = px.scatter(kmeans_pca_df,
                     x="PC1", 
                     y="PC2", 
                     color="K Cluster",
                     title="PC 1 & 2 Biplot")
    fig.update_layout(title_x=0.5)
    
    return fig

  
  
# ~~~ Dash Components ~~~

scree_plot_comp = dcc.Graph(id="scree-plot", className="scree-plot")
slider_header_comp = html.P("Select a PC")
dropdown_comp = dcc.Dropdown(id="scree-dropdown", options=list(range(1,8)), value=1, clearable=False)
k_plot_comp = dcc.Graph(figure=make_k_plot())
biplot_comp = dcc.Graph(figure=make_biplot())
    


# ~~~ App layout ~~~
    
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
                 dbc.Container([
                     dbc.Row([dbc.Col(slider_header_comp, width="auto")]),
                     dbc.Row([dbc.Col(dropdown_comp), dbc.Col(scree_plot_comp, width={"size":11})])
                     ]),
                 ]),
    
    html.Div(className="k-function-plot-div",
             children=[
                 dbc.Container([
                     dbc.Row([dbc.Col(k_plot_comp), dbc.Col(biplot_comp)])])
                ])
])

# ~~~ Callbacks ~~~

@app.callback(Output("scree-plot", "figure"),
              Input("scree-dropdown", "value"))
def scree_plot_graph(n_to_highlight:int):
    fig = make_scree_plot(n_to_highlight)
    return fig


if __name__ == "__main__":
   app.run_server(debug=True)