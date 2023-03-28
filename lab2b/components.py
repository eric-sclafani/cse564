from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import squareform, pdist
from dash import dcc
import pandas as pd 
import plotly.express as px

# ~~~ Global variables ~~~

data_df = pd.read_csv("data/pan22_features.csv")
X = data_df.drop(columns=["author_id", "discourse_type"])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_T_scaled = scaler.fit_transform(X.values.T)

kmeans = KMeans(n_clusters=9, random_state=42)
kmeans.fit(X_scaled)


# ~~~ Helpers ~~~

def get_dissim_matrix_df():
    dis_matrix_df = pd.concat([
        pd.DataFrame(list(X.columns)),
        pd.DataFrame(squareform(pdist(X_T_scaled, metric="correlation")))],
                            axis=1, 
                            ignore_index=True)

    dis_matrix_df.set_index(0, inplace=True)
    dis_matrix_df.columns = list(X.columns)
    return dis_matrix_df

def get_kmeans_df(df):
    """Takes a DataFrame and concatenates it with the kmeans labels"""
    kmeans_df = pd.concat([df, 
                           pd.DataFrame({"K Cluster":kmeans.labels_})],
                          axis=1)
    return kmeans_df

# ~~~ Plot components ~~~

def MDS_data_plot():
    mds_data = MDS(random_state=42)
    embedding_data = mds_data.fit_transform(X_scaled)
    kmeans_embedding_df = get_kmeans_df(pd.DataFrame({"Component 1":embedding_data[:,0],"Component 2":embedding_data[:,1]}))
    fig = px.scatter(
        kmeans_embedding_df, 
        x="Component 1", 
        y="Component 2", 
        color="K Cluster")
    
    fig.update_layout(
        title="Data MDS Plot",
        title_x=0.5)
    
    return fig

def pcp_all_dims_plot():
    data_df_sample = data_df.sample(n=15, axis="columns",random_state=42)
    kmeans_pcp_df = get_kmeans_df(data_df_sample)
    fig = px.parallel_coordinates(
        kmeans_pcp_df,
        dimensions=list(data_df_sample.columns),
        color="K Cluster",
        title="PCP All Dimensions")
    fig.update_layout(title_x=0.5)
    return fig


def MDS_variables_plot():
    
    dis_matrix_df = get_dissim_matrix_df()
    mds_variables = MDS(random_state=42, dissimilarity="precomputed")
    embedding_variables = mds_variables.fit_transform(dis_matrix_df.values)
    
    variables_df = pd.DataFrame({
        "Feature name": dis_matrix_df.columns,
        "Component 1":embedding_variables[:,0],
        "Component 2":embedding_variables[:,1]})

    fig = px.scatter(
        variables_df, 
        x="Component 1", 
        y="Component 2",
        text="Feature name")
    fig.update_layout(title="Variables MDS Plot",
                      title_x=0.5)
    fig.update_traces(textfont_size=7.5)
    return fig

def mds_pcp_variables_plot():
    dims_to_show = ["H", 
                    "over", 
                    "('ADJ', 'ADP')", 
                    "('ADV', 'the')", 
                    "were", 
                    "('VERB', 'PUNCT')", 
                    "pcomp", 
                    "('NOUN', 'have')", 
                    "('to', 'NOUN')", 
                    "nsubjpass",
                    "('and', 'NOUN')",
                    "('of', 'NOUN')",
                    "('AUX', 'AUX')",
                    "relcl",
                    "('NOUN', 'CCONJ')"]
    df_subset = data_df[dims_to_show]
    kmeans_df = get_kmeans_df(df_subset)
    fig = px.parallel_coordinates(
        kmeans_df,
        dimensions=df_subset.columns,
        color="K Cluster",
        title="Selected MDS Variables PCP")
    fig.update_layout(title_x=0.5)
    return fig

# ~~~ Other components ~~~

def page2_note():
    return dcc.Markdown("**Note**: _my data has over 400 dimensions, so I randomly (seeded) selected 15 dimensions to display here._")


def page3_note():
    return dcc.Markdown("**Note**: _After spending hours attempting to get the interaction to work in Dash, I was unsuccessful. Instead, I ordered the PCP dimensions manually based on correlations in the MDS variables plot (as suggested by Prof. Mueller)_.")
