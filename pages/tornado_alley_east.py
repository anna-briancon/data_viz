import pandas as pd
import plotly.graph_objs as go

# Charger les données
df_tornadoes = pd.read_csv('us_tornado_dataset_1950_2021.csv')
df_tornadoes['date'] = pd.to_datetime(df_tornadoes['date'])
df_tornadoes['year'] = df_tornadoes['date'].dt.year

# Filtrer les données pour chaque état à partir de 1980
states = ['MO', 'IL', 'IN', 'AR', 'MN']
df_filtered = df_tornadoes[(df_tornadoes['st'].isin(states)) & (df_tornadoes['year'] >= 1980)]

# Grouper les données par année pour chaque état
tornadoes_per_year = df_filtered.groupby(['year', 'st']).size().reset_index(name='tornado_count')

# Calculer la moyenne des tornades par année pour les états sélectionnés
mean_tornadoes_per_year = tornadoes_per_year.groupby('year')['tornado_count'].mean().reset_index(name='mean_tornado_count')

def generate_tornado_count_graph_east():
    filtered_df = mean_tornadoes_per_year

    fig = go.Figure()

    # Ajouter la courbe de la moyenne des tornades
    fig.add_trace(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['mean_tornado_count'],
        mode='lines+markers',
        name='Moyenne des Tornades (MO, IL, IN, AR, MN)',
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