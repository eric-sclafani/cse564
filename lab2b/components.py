from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.preprocessing import StandardScaler
import pandas as pd 
import plotly.express as px

df = pd.read_csv("data/pan22_features.csv")
X = df.drop(columns=["author_id", "discourse_type"])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_T_scaled = scaler.fit_transform(X.values.T)

mds = MDS(random_state=42)
kmeans = KMeans(n_clusters=9, random_state=42)
kmeans.fit(X_scaled)

def MDS_data_plot():
    
    embedding_data = mds.fit_transform(X_scaled)
    kmeans_embedding_df = pd.concat([pd.DataFrame({"Component 1":embedding_data[:,0],"Component 2":embedding_data[:,1]}), 
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


def MDS_variables_plot():
    
    embedding_variables = mds.fit_transform(X_T_scaled)
    variables_df = pd.DataFrame({"Component 1":embedding_variables[:,0],
                                 "Component 2":embedding_variables[:,1]})

    fig = px.scatter(variables_df, 
                    x="Component 1", 
                    y="Component 2")
    fig.update_layout(title="Variables MDS Plot",
                    title_x=0.5)
    return fig

def parallel_coords_plot_task5():
    """Because I have 409 dimensions, I randomly select n dimensions to show"""
    
    kmeans_pcp_df = pd.concat([df.sample(n=10, axis="columns"), 
                               pd.DataFrame({"K Cluster":kmeans.labels_})])
    
    fig = px.parallel_coordinates(
        kmeans_pcp_df,
        color="K Cluster",
    )
    return fig

def parallel_coords_plot_task6():
    pass