import dash_bootstrap_components as dbc
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import pandas as pd 
import numpy as np


df = pd.read_csv("data/pan22_features.csv")
X = df.drop(columns=["author_id", "discourse_type"])

mds = MDS(n_components=2, random_state=42)
embedding = mds.fit_transform(X)

kmeans = KMeans(n_clusters=9, random_state=42)
kmeans.fit(embedding)

mds_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="Multidimensional Scaling  Plots",
    children=[]
)

pcp_tab = dbc.Tab(
    tabClassName="flex-grow-1 text-center",
    label="Parallel Coordinates Plot",
    children=[]
)