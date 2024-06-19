import pandas as pd
import plotly.graph_objs as go

# Charger les données de température
df_temperature = pd.read_csv('temperature.csv')

# Filtrer les données pour la Tornado Alley
states_tornado = ['Oklahoma', 'Kansas', 'Arkansas', 'Iowa', 'Missouri']
df_filtered_temp_tornado = df_temperature[df_temperature['State'].isin(states_tornado)].copy()
df_filtered_temp_tornado['dt'] = pd.to_datetime(df_filtered_temp_tornado['dt'], errors='coerce')
df_filtered_temp_tornado['year'] = df_filtered_temp_tornado['dt'].dt.year
temp_per_year_tornado = df_filtered_temp_tornado.groupby('year')['AverageTemperature'].mean().reset_index()

# Filtrer les données pour la Dixie Valley
states_dixie = ['Arkansas', 'Tennessee', 'Alabama', 'Georgia (State)']
df_filtered_temp_dixie = df_temperature[df_temperature['State'].isin(states_dixie)].copy()
df_filtered_temp_dixie['dt'] = pd.to_datetime(df_filtered_temp_dixie['dt'], errors='coerce')
df_filtered_temp_dixie['year'] = df_filtered_temp_dixie['dt'].dt.year
temp_per_year_dixie = df_filtered_temp_dixie.groupby('year')['AverageTemperature'].mean().reset_index()

# Générer le graphique combiné
def generate_temperature_graph_tornado():
    fig = go.Figure()

    # Ajouter la courbe pour la Tornado Alley
    fig.add_trace(go.Scatter(
        x=temp_per_year_tornado['year'],
        y=temp_per_year_tornado['AverageTemperature'],
        mode='lines+markers',
        name='Tornado Alley',
        line=dict(shape='linear')
    ))

    # Ajouter la courbe pour la Dixie Valley
    fig.add_trace(go.Scatter(
        x=temp_per_year_dixie['year'],
        y=temp_per_year_dixie['AverageTemperature'],
        mode='lines+markers',
        name='Dixie Valley',
        line=dict(shape='linear')
    ))

    fig.update_layout(
        title="Température Moyenne dans la Tornado Alley et la Dixie Valley",
        xaxis_title="Année",
        yaxis_title="Température Moyenne (°C)",
        legend=dict(
            x=1.1,
            y=0.5
        ),
    )

    return fig
