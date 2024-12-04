from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_leaflet as dl
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

def ciudad():
    engine = create_engine('mysql+mysqldb://root:19971995@localhost/INMOBILIARIA')
    query = """
    SELECT 
        c.id_ciudad,
        c.dimensiones,
        c.precios,
        c.direcciones,
        ci.nombre_ciudad,
        z.nombre_zona
    FROM 
        contenedora c
    JOIN 
        ciudad ci ON c.id_ciudad = ci.id_ciudad
    JOIN 
        zona z ON c.id_zona = z.id_zona
    """
    df = pd.read_sql(query, engine)
    return df

def dashboard():
    df = ciudad()

    city = {
        1: [29.072967, -110.955919],
        2: [19.432608, -99.133209],
        3: [17.073185, -96.726589]
    }

    cityinfo = {
        1: 'Sonora',
        2: 'CDMX',
        3: 'Oaxaca'
    }

    layout = html.Div([
        html.H2("📊 Análisis de Mercado Inmobiliario en México", className="custom_p", style={'textAlign': 'center', 'color': 'white'}),

        dcc.Dropdown(
            id='city-dropdown',
            options=[
                {'label': 'Sonora', 'value': 1},
                {'label': 'Ciudad de México', 'value': 2},
                {'label': 'Oaxaca', 'value': 3}
            ],
            value=1,
        ),

        html.Div([
            dl.Map(center=[23.634501, -102.552784], zoom=4.9, children=[
                dl.TileLayer(id="tile-layer"),
                dl.LayerGroup(id='layer')
            ], style={'width': '100%', 'height': '400px', 'margin': "auto", "display": "block"})
        ], style={'marginBottom': '20px'}),

        html.H4("📋 Datos de Propiedades", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='city-table',
            columns=[
                {'name': 'Nombre', 'id': 'nombre_ciudad'},
                {'name': 'Dirección', 'id': 'direcciones'},
                {'name': 'Precio', 'id': 'precios'}
            ],
            data=[],
            style_cell={'textAlign': 'left', 'color': 'white', 'backgroundColor': 'black'},
            style_header={'backgroundColor': 'grey', 'fontWeight': 'bold'},
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),

        html.Div([
            html.Div([
                html.H4("📈 Visualización de Datos", style={'textAlign': 'center'}),
                dcc.Graph(id='price-comparison'),
                html.Div(id='comparison-interpretation', style={'fontSize': '12px'})
            ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top'}),

            html.Div([
                html.H4("📈 Visualización de Datos", style={'textAlign': 'center'}),
                dcc.Graph(id='dimension-price-relation'),
                html.Div(id='dimension-interpretation', style={'fontSize': '12px'})
            ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top'})
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between', 'marginTop': '20px'}),

        html.H4("Análisis visual y intuitivo", style={'textAlign': 'center', 'marginTop': '20px'})
    ])

    return layout

def register_callbacks(app):
    df = ciudad()

    city = {
        1: [29.072967, -110.955919],
        2: [19.432608, -99.133209],
        3: [17.073185, -96.726589]
    }

    cityinfo = {
        1: 'Sonora',
        2: 'CDMX',
        3: 'Oaxaca'
    }

    @app.callback(
        [Output('layer', 'children'),
         Output('city-table', 'data'),
         Output('price-comparison', 'figure'),
         Output('comparison-interpretation', 'children'),
         Output('dimension-price-relation', 'figure'),
         Output('dimension-interpretation', 'children')],
        [Input('city-dropdown', 'value')]
    )
    def interpretacion(selectedcity):
        cityname = cityinfo[selectedcity]
        filtered_df = df[df['nombre_ciudad'] == cityname]

        if filtered_df.empty:
            markers = []
            data_table = [{'nombre_ciudad': 'No hay datos', 'direcciones': 'N/A', 'precios': 'N/A'}]
            comparison_interpretation_text = "No hay datos disponibles para la ciudad seleccionada."
            dimension_interpretation_text = "No hay datos disponibles para la ciudad seleccionada."
        else:
            markers = [dl.Marker(position=city[selectedcity], children=dl.Tooltip(cityname))]

            data_table = filtered_df[['nombre_ciudad', 'direcciones', 'precios']].to_dict('records')

        max_price_zone = df.loc[df['precios'].idxmax()]['nombre_zona']
        max_price = df['precios'].max()
        min_price_zone = df.loc[df['precios'].idxmin()]['nombre_zona']
        min_price = df['precios'].min()
        comparison_interpretation_text = f"Comparando los precios entre las zonas de Sonora, CDMX y Oaxaca, se observa que la zona {max_price_zone} tiene una mayor concentración de propiedades con precios altos ${max_price} millones de pesos, mientras que la zona {min_price_zone} tiene una mayor concentración de propiedades con precios bajos ${min_price}00000 mil pesos en este caso menos de un millon."

        dimension_interpretation_text = f"Al examinar la relación entre las dimensiones y los precios de las propiedades en Sonora, CDMX y Oaxaca, se puede apreciar una tendencia interesante: las propiedades de mayor tamaño suelen tener precios más elevados. Esta observación indica una correlación positiva entre el tamaño de las propiedades y su valor en el mercado. Este patrón sugiere que los compradores valoran significativamente el espacio adicional, lo cual se refleja en el precio final de las propiedades."

        price_comparison_fig = px.bar(df, x='nombre_zona', y='precios', color='nombre_ciudad',
                                      title="Comparación de Precios entre Zonas")

        dimension_price_relation_fig = px.scatter(df, x='dimensiones', y='precios', color='nombre_ciudad',
                                                  title="Relación entre Dimensiones y Precios")

        return markers, data_table, price_comparison_fig, comparison_interpretation_text, dimension_price_relation_fig, dimension_interpretation_text
