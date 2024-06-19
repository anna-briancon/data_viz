import pandas as pd
import plotly.graph_objs as go

# Charger et filtrer les données de température
df_temperature = pd.read_csv('temperature.csv')

# Filtre pour les états de la Dixie Valley
states = ['Arkansas', 'Tennessee', 'Alabama', 'Georgia (State)']
df_filtered_temp = df_temperature[df_temperature['State'].isin(states)].copy()

df_filtered_temp['dt'] = pd.to_datetime(df_filtered_temp['dt'], errors='coerce')
df_filtered_temp['year'] = df_filtered_temp['dt'].dt.year

# Calculer la température moyenne par année pour tous les états
temp_per_year = df_filtered_temp.groupby('year')['AverageTemperature'].mean().reset_index()

def generate_temperature_graph_dixie():
    fig = go.Figure()

    # Ajouter la courbe pour la température moyenne agrégée
    fig.add_trace(go.Scatter(
        x=temp_per_year['year'],
        y=temp_per_year['AverageTemperature'],
        mode='lines+markers',
        name='Température Moyenne (Tous les États)',
        line=dict(shape='linear')
    ))

    fig.update_layout(
        title="Température Moyenne dans la Dixie Valley",
        xaxis_title="Année",
        yaxis_title="Température Moyenne (°C)",
        legend=dict(
            x=1.1,
            y=0.5
        ),
    )

    return fig