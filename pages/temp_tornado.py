import pandas as pd
import plotly.graph_objs as go

# Charger et filtrer les données de température
df_temperature = pd.read_csv('temperature.csv')

# Filtre pour les états de la Dixie Valley
states = ['Oklahoma', 'Kansas', 'Arkansas', 'Iowa', 'Missouri']
df_filtered_temp = df_temperature[df_temperature['State'].isin(states)].copy()

df_filtered_temp['dt'] = pd.to_datetime(df_filtered_temp['dt'], errors='coerce')
df_filtered_temp['year'] = df_filtered_temp['dt'].dt.year

temp_per_year_state = df_filtered_temp.groupby(['year', 'State'])['AverageTemperature'].mean().reset_index()

def generate_temperature_graph_tornado():
    fig = go.Figure()

    # Ajouter les courbes pour chaque état
    for state in states:
        state_df = temp_per_year_state[temp_per_year_state['State'] == state]
        fig.add_trace(go.Scatter(
            x=state_df['year'],
            y=state_df['AverageTemperature'],
            mode='lines+markers',
            name=f'Température Moyenne ({state})',
            line=dict(shape='linear')
        ))

    fig.update_layout(
        title="Température Moyenne par État dans la Tornado Alley",
        xaxis_title="Année",
        yaxis_title="Température Moyenne (°C)",
        legend=dict(
            x=1.1,
            y=0.5
        ),
    )

    return fig
