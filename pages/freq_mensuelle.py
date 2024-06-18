import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

df = pd.read_csv('us_tornado_dataset_1950_2021.csv')

df['date'] = pd.to_datetime(df['date'])

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

df_before_2000 = df[(df['year'] >= 1980) & (df['year'] < 2000)]
df_after_2000 = df[df['year'] >= 2000]

freq_before_2000 = df_before_2000.groupby('month').size().reindex(range(1, 13), fill_value=0)
freq_after_2000 = df_after_2000.groupby('month').size().reindex(range(1, 13), fill_value=0)

years_before_2000 = df_before_2000['year'].nunique()
years_after_2000 = df_after_2000['year'].nunique()

avg_freq_before_2000 = freq_before_2000 / years_before_2000
avg_freq_after_2000 = freq_after_2000 / years_after_2000

freq_df = pd.DataFrame({
    'Mois': range(1, 13),
    'Avant 2000': avg_freq_before_2000.values,
    'Après 2000': avg_freq_after_2000.values
})

freq_df = freq_df.melt(id_vars='Mois', var_name='Periode', value_name='Frequence')