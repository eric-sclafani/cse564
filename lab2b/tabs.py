import dash_bootstrap_components as dbc
from dash import dcc, html
import components as comps


mds_data_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="MDS Data Plot",
    children=[
        dbc.Container([
            dbc.Row([dbc.Col(dcc.Graph(figure=comps.MDS_data_plot()))])])
    ]
)

pcp_all_dims_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="PCP All Dimensions Plot",
    children=[
        html.Div(className="page2-note-div", children=[comps.page2_note()]),
        dcc.Graph(figure=comps.pcp_all_dims_plot()),
        ]
)

mds_pcp_variables_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="MDS + PCP Variables Plots",
    children=[
        dbc.Container([
            dbc.Row([dbc.Col(html.P(comps.page3_note(), className="page3-note"))]),
            dbc.Row([dbc.Col(dcc.Graph(figure=comps.MDS_variables_plot()))]),
            dbc.Row([dbc.Col(dcc.Graph(figure=comps.mds_pcp_variables_plot()))])
        ])
    ]
)