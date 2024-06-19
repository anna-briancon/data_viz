import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Charger les données des tornades
df_tornadoes = pd.read_csv('us_tornado_dataset_1950_2021.csv')
df_tornadoes['date'] = pd.to_datetime(df_tornadoes['date'])
df_tornadoes['year'] = df_tornadoes['date'].dt.year

# Filtrer les données pour chaque état à partir de 1980
states_dixie = ['AR', 'TN', 'AL', 'GA']
df_filtered = df_tornadoes[(df_tornadoes['st'].isin(states_dixie)) & (df_tornadoes['year'] >= 1980)]

# Simulation de données de magnitude (remplacez par vos propres données)
df_magnitude = pd.DataFrame({
    'year': df_tornadoes['year'],
    'st': df_tornadoes['st'],
    'mag': df_tornadoes['mag'].apply(lambda x: x if x >= 0 else None)  # Ignorer les valeurs de magnitude négatives
})

def generate_mag_count_graph_dixie(selected_state):
    filtered_df = df_magnitude[df_magnitude['st'] == selected_state]
    
    # Créer un DataFrame pour compter le nombre de tornades par année et par magnitude
    df_counts = filtered_df.groupby(['year', 'mag']).size().reset_index(name='count')
    
    # Créer une liste pour stocker les barres de chaque magnitude
    data = []
    for mag in range(6):  # Boucle de 0 à 5 pour les magnitudes
        df_mag = df_counts[df_counts['mag'] == mag]
        data.append(go.Bar(
            x=df_mag['year'],
            y=df_mag['count'],
            name=f'Magnitude {mag}',
        ))
    
    fig = go.Figure(data=data)
    
    fig.update_layout(
        title=f"Nombre de Tornades par Magnitude pour l'État {selected_state} (1980 - 2021)",
        xaxis_title="Année",
        yaxis_title="Nombre de Tornades",
        barmode='stack',  # Pour empiler les barres les unes sur les autres
        legend=dict(
            x=1.1,
            y=0.5
        ),
    )

    return fig