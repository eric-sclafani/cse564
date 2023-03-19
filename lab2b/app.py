
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import CERULEAN
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import pandas as pd 
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # suppress annoying kmeans future warning