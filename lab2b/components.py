from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("data/pan22_features.csv")
X = df.drop(columns=["author_id", "discourse_type"])

mds = MDS(random_state=42)
kmeans = KMeans(n_clusters=9, random_state=42)
kmeans.fit(X)

def MDS_data_plot() -> go.Figure:
    
    embedding = mds.fit_transform(X)
    kmeans_embedding_df = pd.concat([pd.DataFrame({"Component 1":embedding[:,0],"Component 2":embedding[:,1]}), 
                                     pd.DataFrame({"K Cluster":kmeans.labels_})], 
                                    axis=1)
    fig = px.scatter(
        kmeans_embedding_df, 
        x="Component 1", 
        y="Component 2", 
        color="K Cluster")
    
    fig.update_layout(
        title="Data MDS Plot",
        title_x=0.5)
    
    return fig