import dash_bootstrap_components as dbc
from dash import dcc, html
import components as comps


mds_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="Multidimensional Scaling Plots",
    children=[
        dcc.Graph(figure=comps.MDS_data_plot()),
    ]
)

pcp_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="Parallel Coordinates Plots",
    children=[
        dcc.Graph(figure=comps.parallel_coords_plot_task5()),
        ]
)