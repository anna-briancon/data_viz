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


#
#
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

states = ['OK', 'KS', 'AR', 'IA', 'MO', 'TX', 'CO', 'MN', 'SD', 'IL', 'IN', 'NE']

df_filtered = df_tornadoes[(df_tornadoes['st'].isin(states)) & (df_tornadoes['year'] >= 1980)]

# Grouper les données par année pour chaque état
tornadoes_per_year = df_filtered.groupby(['year', 'st']).size().reset_index(name='tornado_count')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Évolution du Nombre de Tornades par État dans la Tornado Alley (1980 - 2021)"),
    
    html.Label("Sélectionner une option"),
    dcc.Dropdown(
        id='decade-dropdown',
        options=[
            {'label': f'{i}s', 'value': i} for i in range(1980, 2030, 10)
        ] + [{'label': 'Toutes les décennies', 'value': 'all'}],
        value='all'
    ),
    
    dcc.Graph(id='tornado-count-graph')
])

@app.callback(
    Output('tornado-count-graph', 'figure'),
    Input('decade-dropdown', 'value')
)
def update_tornado_count_graph(selected_decade):
    if selected_decade == 'all':
        filtered_df = tornadoes_per_year
    else:
        filtered_df = tornadoes_per_year[(tornadoes_per_year['year'] >= selected_decade) & (tornadoes_per_year['year'] < selected_decade + 10)]
    
    fig = go.Figure()

    # Ajouter les courbes pour chaque état
    for state in states:
        state_df = filtered_df[filtered_df['st'] == state]
        fig.add_trace(go.Scatter(
            x=state_df['year'],
            y=state_df['tornado_count'],
            mode='lines+markers',
            name=f'Nombre de Tornades ({state})',
            line=dict(shape='linear')
        ))

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

if __name__ == '__main__':
    app.run_server(debug=True)
