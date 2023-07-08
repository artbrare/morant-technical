import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

sns.set(style="darkgrid")

# Carga de datos
injuries = pd.read_csv("injuries.tsv", sep="\t")
products = pd.read_csv("products.tsv", sep="\t")
population = pd.read_csv("population.tsv", sep="\t")

prod_codes = dict(zip(products['prod_code'], products['title']))

# Configuración de la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='code-dropdown',
            options=[{'label': value, 'value': key}
                     for key, value in prod_codes.items()],
            value=649
        ),
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[
                {'label': 'Número estimado de lesiones', 'value': 'count'},
                {'label': 'Lesiones por cada 10,000 personas', 'value': 'rate'}
            ],
            value='count'
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        html.Div([
            html.H3("Tabla de diagnósticos"),
            dcc.Graph(id='diag-table')
        ], className='four columns'),
        html.Div([
            html.H3("Tabla de partes del cuerpo"),
            dcc.Graph(id='body-part-table')
        ], className='four columns'),
        html.Div([
            html.H3("Tabla de ubicaciones"),
            dcc.Graph(id='location-table')
        ], className='four columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.H3("Número estimado de lesiones por edad y sexo"),
            dcc.Graph(id='age-sex-plot')
        ], className='twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.H3("Tasa de lesiones por edad y sexo"),
            dcc.Graph(id='age-sex-rate-plot')
        ], className='twelve columns')
    ], className='row')
])


@app.callback(
    dash.dependencies.Output('diag-table', 'figure'),
    dash.dependencies.Output('body-part-table', 'figure'),
    dash.dependencies.Output('location-table', 'figure'),
    dash.dependencies.Output('age-sex-plot', 'figure'),
    dash.dependencies.Output('age-sex-rate-plot', 'figure'),
    [dash.dependencies.Input('code-dropdown', 'value')]
)
def update_tables_and_plots(product_code):
    # Filtrar el conjunto de datos de lesiones para el código de
    # producto seleccionado
    selected = injuries[injuries['prod_code'] == product_code]

    # Tablas
    diag_counts = selected.groupby('diag')['weight'].sum(
    ).reset_index().sort_values(by='weight', ascending=False)
    body_part_counts = selected.groupby('body_part')['weight'].sum(
    ).reset_index().sort_values(by='weight', ascending=False)
    location_counts = selected.groupby('location')['weight'].sum(
    ).reset_index().sort_values(by='weight', ascending=False)

    diag_table = go.Figure(data=[go.Table(
        header=dict(values=['Diagnóstico', 'Peso estadístico']),
        cells=dict(values=[diag_counts['diag'], diag_counts['weight']])
    )])

    body_part_table = go.Figure(data=[go.Table(
        header=dict(values=['Parte del cuerpo', 'Peso estadístico']),
        cells=dict(values=[body_part_counts['body_part'],
                   body_part_counts['weight']])
    )])

    location_table = go.Figure(data=[go.Table(
        header=dict(values=['Ubicación', 'Peso estadístico']),
        cells=dict(values=[location_counts['location'],
                   location_counts['weight']])
    )])

    # Gráficas
    summary = selected.groupby(['age', 'sex'], as_index=False)['weight'].sum()
    age_sex_plot = px.line(summary, x='age', y='weight', color='sex',
                           title='Número estimado de lesiones por edad y sexo')
    age_sex_plot.update_xaxes(title='Age')
    age_sex_plot.update_yaxes(title='Número estimado de lesiones')

    summary = summary.merge(population, on=['age', 'sex'])
    summary['rate'] = (summary['weight'] / summary['population']) * 10000

    age_sex_rate_plot = px.line(summary, x='age', y='rate', color='sex',
                                title='Tasa de lesiones por edad y sexo')
    age_sex_rate_plot.update_xaxes(title='Age')
    age_sex_rate_plot.update_yaxes(title='Lesiones por cada 10.000 personas')

    return diag_table, body_part_table, location_table, age_sex_plot,
    age_sex_rate_plot


if __name__ == '__main__':
    app.run_server(debug=True)
