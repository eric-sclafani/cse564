from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist
import pandas as pd 
import plotly.express as px

data_df = pd.read_csv("data/pan22_features.csv")
X = data_df.drop(columns=["author_id", "discourse_type"])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_T_scaled = scaler.fit_transform(X.values.T)

# dissimilarity matrix
dis_matrix_df = pd.concat([
    pd.DataFrame(list(X.columns)),
    pd.DataFrame(squareform(pdist(X_T_scaled, metric="correlation")))],
                          axis=1, 
                          ignore_index=True)

dis_matrix_df.set_index(0, inplace=True)
dis_matrix_df.columns = list(X.columns)

kmeans = KMeans(n_clusters=9, random_state=42)
kmeans.fit(X_scaled)

def MDS_data_plot():
    
    mds_data = MDS(random_state=42)
    embedding_data = mds_data.fit_transform(X_scaled)
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
    
    mds_variables = MDS(random_state=42, dissimilarity="precomputed")
    embedding_variables = mds_variables.fit_transform(dis_matrix_df.values)
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
    
    data_df_sample = data_df.sample(n=10, axis="columns",random_state=42)
    kmeans_pcp_df = pd.concat([data_df_sample, 
                               pd.DataFrame({"K Cluster":kmeans.labels_})],
                              axis=1)
    
    fig = px.parallel_coordinates(
        kmeans_pcp_df,
        dimensions=list(data_df_sample.columns),
        color="K Cluster",
    )
    return fig

def parallel_coords_plot_task6():
    pass