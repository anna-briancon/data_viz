import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

df_tornadoes = pd.read_csv('us_tornado_dataset_1950_2021.csv')
df_tornadoes['date'] = pd.to_datetime(df_tornadoes['date'])
df_tornadoes['year'] = df_tornadoes['date'].dt.year

df_co2 = pd.read_csv('ges.csv')
df_temperature = pd.read_csv('temperature.csv')  

df_temperature['dt'] = pd.to_datetime(df_temperature['dt'])
df_temperature.set_index('dt', inplace=True)

df_temperature_april_june = df_temperature[(df_temperature.index.month >= 4) & (df_temperature.index.month <= 6) & (df_temperature['Country'] == 'United States')]

avg_temperature_per_year = df_temperature_april_june.groupby(df_temperature_april_june.index.year)['AverageTemperature'].mean().reset_index()
avg_temperature_per_year.columns = ['year', 'AverageTemperature']

tornadoes_per_year = df_tornadoes.groupby('year').size().reset_index(name='tornado_count')
tornadoes_per_year = tornadoes_per_year[tornadoes_per_year['year'] >= 1990]

df_co2 = df_co2[['U.S. Emissions by Economic Sector, MMT CO2 eq.', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']]
df_co2 = df_co2.set_index('U.S. Emissions by Economic Sector, MMT CO2 eq.').T
df_co2.index = df_co2.index.astype(int)
df_co2.reset_index(inplace=True)
df_co2.columns = ['year', 'co2_emissions']

df_combined = pd.merge(tornadoes_per_year, df_co2, on='year', how='inner')
df_combined = pd.merge(df_combined, avg_temperature_per_year, on='year', how='inner')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Impact du Réchauffement Climatique : Tornades et Température aux USA"),
    
    html.Label("Sélectionner une option"),
    dcc.Dropdown(
        id='decade-dropdown',
        options=[
            {'label': f'{i}s', 'value': i} for i in range(1990, 2030, 10)
        ] + [{'label': 'Toutes les décennies', 'value': 'all'}],
        value='all'
    ),
    
    dcc.Graph(id='co2-temperature-graph'),
    dcc.Graph(id='temperature-tornado-graph')
])

@app.callback(
    Output('co2-temperature-graph', 'figure'),
    Input('decade-dropdown', 'value')
)
def update_co2_temperature_graph(selected_decade):
    if selected_decade == 'all':
        filtered_df = df_combined
    else:
        filtered_df = df_combined[(df_combined['year'] >= selected_decade) & (df_combined['year'] < selected_decade + 10)]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['co2_emissions'],
        mode='lines+markers',
        name='Émissions de CO2',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['AverageTemperature'],
        mode='lines+markers',
        name='Température Moyenne',
        line=dict(color='green'),
        yaxis='y2'  
    ))

    fig.update_layout(
        title="Impact du Réchauffement Climatique : Émissions de CO2 et Température Moyenne aux USA",
        xaxis_title="Année",
        yaxis_title="Émissions de CO2 (MMT)",
        yaxis2=dict(
            title="Température Moyenne (°C)",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(
            x=1.1,  
            y=0.5  
        ),
    )

    return fig

@app.callback(
    Output('temperature-tornado-graph', 'figure'),
    Input('decade-dropdown', 'value')
)
def update_temperature_tornado_graph(selected_decade):
    if selected_decade == 'all':
        filtered_df = df_combined
    else:
        filtered_df = df_combined[(df_combined['year'] >= selected_decade) & (df_combined['year'] < selected_decade + 10)]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['AverageTemperature'],
        mode='lines+markers',
        name='Température Moyenne',
        line=dict(color='green')
    ))

    fig.add_trace(go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['tornado_count'],
        mode='lines+markers',
        name='Nombre de Tornades',
        line=dict(color='red'),
        yaxis='y2'
    ))

    fig.update_layout(
        title="Impact du Réchauffement Climatique : Température Moyenne et Nombre de Tornades aux USA",
        xaxis_title="Année",
        yaxis_title="Température Moyenne (°C)",
        yaxis2=dict(
            title="Nombre de Tornades",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(
            x=1.1,  
            y=0.5  
        ),
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
