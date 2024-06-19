import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pages.freq_mensuelle import freq_df
from pages.localisation import df_heatmap
from pages.tornado_alley_west import generate_tornado_count_graph_west
from pages.tornado_alley_east import generate_tornado_count_graph_east
from pages.puissance_tornado_alley_west import generate_mag_count_graph_west, states
from pages.puissance_tornado_dixie import generate_mag_count_graph_dixie, states_dixie
from pages.dixie_alley import generate_tornado_count_graph_dixie
from pages.temp_dixie import generate_temperature_graph_dixie
from pages.temp_tornado import generate_temperature_graph_tornado
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Le réchauffement climatique a-t-il un impact sur les tornades aux USA", className='text-center mt-5 mb-4'),
    html.H3("Analyse des tendances et des déplacements des tornades dans Tornado Alley", className='text-center mb-5'),

    html.H2("Sommaire", className='mb-4'),
    dbc.ListGroup([
        dbc.ListGroupItem("1 - Contexte"),
        dbc.ListGroupItem("2 - Tendances et Changements Récents"),
        dbc.ListGroupItem("3 - Conclusion")
    ], flush=True),

    html.H2("1 - Contexte", className='mb-4 mt-5 text-center'),
    dbc.Col([
        html.H4("Tornado Alley"),
        html.P("La Tornado Alley s'étend du nord du Texas au Dakota du Sud, en passant par l'Oklahoma, le Kansas et le Nebraska."),
        html.Img(src='/assets/Tornado_Alley_Diagram_fr.svg.png', className='img-fluid')
    ], md=6, className='mx-auto'),

    dbc.Col([
        html.H4("Dixie Alley"),
        html.P("La Dixie Alley s'étend de l'Arkansas à la Géorgie, en passant par le Mississippi, la Louisiane, le Tennessee et l'Alabama."),
        html.Img(src='/assets/dixie_alley.jpg', className='img-fluid')
    ], md=6, className='mx-auto'),

    html.Br(),

    dbc.Col([
        html.H4("Saison des tornades"),
        html.P("Avril à juin"),
        html.P("Graphique montrant le nombre moyen de tornades par mois de 1950 à 2021 : "),
        html.Img(src='assets/average_tornadoes_per_month.png', className='img-fluid')
    ], md=6, className='mx-auto'),

    html.H2("2 - Tendances et Changements Récents", className='mb-4 mt-5 text-center'),
    dbc.Col([
        html.H4("Fréquence et Période des Tornades"),
        html.P("Graphique de la fréquence mensuelle des tornades, comparant les périodes avant et après les années 2000 : "),
        dcc.Checklist(
            id='periode-selector',
            options=[
                {'label': 'Avant 2000', 'value': 'Avant 2000'},
                {'label': 'Après 2000', 'value': 'Après 2000'}
            ],
            value=['Avant 2000', 'Après 2000'],  
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='monthly-tornado-frequency'),
    ], md=6, className='mx-auto'),

    dbc.Col([
        html.H4("Localisation des Tornades"),
        dcc.Dropdown(
            id='decade-dropdown',
            options=[{'label': decade, 'value': decade} for decade in sorted(df_heatmap['decade'].unique())] + [{'label': 'Tout', 'value': 'all'}],
            value='all',
            clearable=False
        ),
        dcc.Graph(id='tornado-heatmap')
    ], md=6, className='mx-auto'),

    dbc.Col([
        html.H4("Nombre de Tornades par État dans la Tornado Alley - Ouest"),
        dcc.Graph(id='tornado-count-graph-west'),
    ], md=6, className='mx-auto'),

    dbc.Col([
        html.H4("Température Moyenne dans les régions de tornades"),
        dcc.Graph(id='temperature-graph-tornado'),
    ], md=6, className='mx-auto'),

    dbc.Col([
        html.H4("Évolution du coefficient des tornades par État dans la Tornado Alley - Ouest (1980 - 2021)"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in states],
            value=states[0],
            clearable=False,
            style={'width': '50%'} 
        ),
        dcc.Graph(id='mag-count-graph-west'),
        html.H4("Évolution du coefficient des tornades par État dans la Dixie Alley (1980 - 2021)"),
        dcc.Dropdown(
            id='state-dropdown2',
            options=[{'label': state, 'value': state} for state in states_dixie],
            value=states[0],
            clearable=False,
            style={'width': '50%'} 
        ),
        dcc.Graph(id='mag-count-graph-dixie')
    ], md=6, className='mx-auto'),

    dbc.Col([
        dcc.Store(id='dummy-input', data=0) 
    ], md=6, className='mx-auto'),
    
    dbc.Col([
        html.H2("3 - Conclusion", className='mb-4 mt-5 text-center'),
        html.Img(src='assets/tornades-img.avif', className='img-fluid mx-auto d-block mb-500'),
    ], md=6, className='mx-auto mb-5'),
], fluid=True)

@app.callback(
    Output('monthly-tornado-frequency', 'figure'),
    [Input('periode-selector', 'value')]
)
def update_graph(selected_periods):
    filtered_df = freq_df[freq_df['Periode'].isin(selected_periods)]
    
    fig = go.Figure()
    
    for periode in selected_periods:
        fig.add_trace(go.Scatter(
            x=filtered_df[filtered_df['Periode'] == periode]['Mois'],
            y=filtered_df[filtered_df['Periode'] == periode]['Frequence'],
            mode='lines+markers',
            name=periode
        ))
    
    fig.update_layout(
        title='Fréquence mensuelle des tornades avant et après 2000',
        xaxis_title='Mois',
        yaxis_title='Nombre de tornades',
        xaxis=dict(tickvals=list(range(1, 13)), ticktext=['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec'])
    )
    
    return fig

@app.callback(
    Output('tornado-heatmap', 'figure'),
    [Input('decade-dropdown', 'value')]
)
def update_heatmap(selected_decade):
    if selected_decade == 'all':
        data = df_heatmap
        title = 'Distribution géographique des tornades pour toutes les décennies :'
    else:
        data = df_heatmap[df_heatmap['decade'] == selected_decade]
        title = f'Distribution géographique des tornades pour la décennie {selected_decade}'
    
    fig = px.scatter_geo(data, lat='slat', lon='slon', color='decade',
                         color_continuous_scale='viridis', 
                         projection='albers usa', title=title)

    fig.update_layout(geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showland=True,
        landcolor='rgb(217, 217, 217)',
        subunitwidth=1,
        countrywidth=1,
        subunitcolor='rgb(255, 255, 255)',
        countrycolor='rgb(255, 255, 255)'
    ))

    return fig

@app.callback(
    Output('tornado-count-graph-west', 'figure'),
    [Input('dummy-input', 'data')]
)
def update_tornado_count_graph_west(dummy_input):
    return generate_tornado_count_graph_west()

@app.callback(
    Output('temperature-graph-tornado', 'figure'),
    [Input('dummy-input', 'data')]
)
def update_temperature_graph_tornado(dummy_input):
    return generate_temperature_graph_tornado()

@app.callback(
    Output('mag-count-graph-west', 'figure'),
    [Input('state-dropdown', 'value')]
)
def update_mag_count_graph_west(selected_state):
    if selected_state is None:
        raise dash.exceptions.PreventUpdate
    
    fig = generate_mag_count_graph_west(selected_state)
    
    return fig

@app.callback(
    Output('mag-count-graph-dixie', 'figure'),
    [Input('state-dropdown2', 'value')]
)
def update_mag_count_graph_dixie(selected_state):
    if selected_state is None:
        selected_state = states_dixie[0]
    
    fig = generate_mag_count_graph_dixie(selected_state)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
