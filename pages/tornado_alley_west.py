# Tradtionnellement, la région la plus connue pour ses tornades est la Tornado Alley.
# Pleinement intégrés : Oklahoma, Kansas, Arkansas, Iowa, Missouri
# Partiellement intégrés : Texas, Colorado, Minnesota, Dakota du Sud, Illinois, Indiana, Nebrasqua
#
# On évite de répéter des états de la Dixie Alley.
# Pas de tendance à la hausse significative dans les états limitrophes.
# Sauf peut-être le Minnesota (MN), Illinois (IL), tous deux à l'est de la Tornado Alley.
#
# INTEGRES states = ['OK', 'KS', 'AR', 'IA', 'MO']
# PARTIELS states = ['TX', 'CO', 'MN', 'SD', 'IL', 'IN', 'NE']

import pandas as pd
import plotly.graph_objs as go

# Charger les données
df_tornadoes = pd.read_csv('us_tornado_dataset_1950_2021.csv')
df_tornadoes['date'] = pd.to_datetime(df_tornadoes['date'])
df_tornadoes['year'] = df_tornadoes['date'].dt.year

# Définir les états pour chaque région
states_east = ['MO', 'IL', 'IN', 'AR', 'MN']
states_west = ['CO', 'NE', 'OK', 'KS', 'TX']
states_dixie = ['AR', 'TN', 'AL', 'GA']

# Filtrer les données pour chaque région à partir de 1980
df_filtered_east = df_tornadoes[(df_tornadoes['st'].isin(states_east)) & (df_tornadoes['year'] >= 1980)]
df_filtered_west = df_tornadoes[(df_tornadoes['st'].isin(states_west)) & (df_tornadoes['year'] >= 1980)]
df_filtered_dixie = df_tornadoes[(df_tornadoes['st'].isin(states_dixie)) & (df_tornadoes['year'] >= 1980)]

# Grouper les données par année pour chaque région
tornadoes_per_year_east = df_filtered_east.groupby(['year', 'st']).size().reset_index(name='tornado_count')
tornadoes_per_year_west = df_filtered_west.groupby(['year', 'st']).size().reset_index(name='tornado_count')
tornadoes_per_year_dixie = df_filtered_dixie.groupby(['year', 'st']).size().reset_index(name='tornado_count')

# Calculer la moyenne des tornades par année pour les régions sélectionnées
mean_tornadoes_per_year_east = tornadoes_per_year_east.groupby('year')['tornado_count'].mean().reset_index(name='mean_tornado_count')
mean_tornadoes_per_year_west = tornadoes_per_year_west.groupby('year')['tornado_count'].mean().reset_index(name='mean_tornado_count')
mean_tornadoes_per_year_dixie = tornadoes_per_year_dixie.groupby('year')['tornado_count'].mean().reset_index(name='mean_tornado_count')

def generate_tornado_count_graph_west():
    fig = go.Figure()

    # Ajouter la courbe de la moyenne des tornades pour la région Est
    fig.add_trace(go.Scatter(
        x=mean_tornadoes_per_year_east['year'],
        y=mean_tornadoes_per_year_east['mean_tornado_count'],
        mode='lines+markers',
        name='Tornado Alley - Est',
        line=dict(shape='linear')
    ))

    # Ajouter la courbe de la moyenne des tornades pour la région Ouest
    fig.add_trace(go.Scatter(
        x=mean_tornadoes_per_year_west['year'],
        y=mean_tornadoes_per_year_west['mean_tornado_count'],
        mode='lines+markers',
        name='Tornado Alley - Ouest',
        line=dict(shape='linear')
    ))

    # Ajouter la courbe de la moyenne des tornades pour la Dixie Alley
    fig.add_trace(go.Scatter(
        x=mean_tornadoes_per_year_dixie['year'],
        y=mean_tornadoes_per_year_dixie['mean_tornado_count'],
        mode='lines+markers',
        name='Dixie Alley',
        line=dict(shape='linear')
    ))

    fig.update_layout(
        title="Moyenne du Nombre de Tornades par Année (1980 - 2021)",
        xaxis_title="Année",
        yaxis_title="Nombre de Tornades Moyenne",
        legend=dict(
            x=1.1,  
            y=0.5  
        ),
    )

    return fig
