# Les tornades semblent se déplacer vers la côte est, sur la vallée du fleuve du Mississippi.
# C'est ce qu'on appelle la Dixie Alley : Arkansas, Mississippi, Louisiane, Tennessee, Alabama, Géorgie.
# 
# Pleinement intégrés : AR, MI, LA 
# Partiellement : TN, AL, GA (toutes à l'est)
# 
# On constate l'augmentation des tornades à l'est

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Charger et filtrer les données pour les tornades
df_tornadoes = pd.read_csv('us_tornado_dataset_1950_2021.csv')
df_tornadoes['date'] = pd.to_datetime(df_tornadoes['date'])
df_tornadoes['year'] = df_tornadoes['date'].dt.year

# Filtrer les données pour chaque état à partir de 1980
states = ['AR', 'TN', 'AL', 'GA']
states_names = ['Arkansas', 'Tennessee', 'Alabama', 'Géorgie']
df_filtered = df_tornadoes[(df_tornadoes['st'].isin(states)) & (df_tornadoes['year'] >= 1980)]

# Grouper les données par année pour chaque état
tornadoes_per_year = df_filtered.groupby(['year', 'st']).size().reset_index(name='tornado_count')

def generate_tornado_count_graph_dixie():
    filtered_df = tornadoes_per_year    

    fig = go.Figure()

    # Ajouter les courbes pour chaque état
    i = 0
    for state in states:
        state_df = filtered_df[filtered_df['st'] == state]
        fig.add_trace(go.Scatter(
            x=state_df['year'],
            y=state_df['tornado_count'],
            mode='lines+markers',
            name=f'Nombre de Tornades ({states_names[i]})',
            line=dict(shape='linear')
        ))
        i += 1

    fig.update_layout(
        title="Nombre de Tornades par État (1980 - 2021)",
        xaxis_title="Année",
        yaxis_title="Nombre de Tornades",
        legend=dict(
            x=1.1,  
            y=0.5  
        ),
    )

    return fig