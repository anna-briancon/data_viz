import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv('us_tornado_dataset_1950_2021.csv')
df['year'] = df['yr']
df_heatmap = df[['slat', 'slon', 'year']].copy()

def get_decade(year):
    return f"{year // 10 * 10}-{year // 10 * 10 + 9}"

df_heatmap['decade'] = df_heatmap['year'].apply(get_decade)