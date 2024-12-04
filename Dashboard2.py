import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
from sqlalchemy import create_engine

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "19971995",
    "database": "INMOBILIARIA"
}

DATABASE_URI = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:3306/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URI)


def cargar_datos():
    query = """
    SELECT 
        z.nombre_zona AS Zona,
        c.precios AS Precios
    FROM contenedora c
    JOIN zona z ON c.id_zona = z.id_zona;
    """
    try:
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        print(f"Error al cargar datos desde la base de datos: {e}")
        return pd.DataFrame()


data = cargar_datos()


def layout_dashboard():
    return dbc.Container(
        [
            html.H1("📊 Propiedades Comprables por Rango de Presupuesto", style={"textAlign": "center"}),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Rango de Presupuesto:"),
                                dcc.Dropdown(
                                    id="dropdown_rango_presupuesto",
                                    options=[
                                        {"label": "$400,000 a $1,000,000", "value": 400000},
                                        {"label": "$1,000,000 a $2,000,000", "value": 1000000},
                                        {"label": "$2,000,000 a $3,000,000", "value": 2000000},
                                        {"label": "$3,000,000 a $4,000,000", "value": 3000000},
                                        {"label": "$4,000,000 a $5,000,000", "value": 4000000},
                                        {"label": "$5,000,000 a $6,000,000", "value": 5000000},
                                        {"label": "$6,000,000 a $7,000,000", "value": 6000000},
                                        {"label": "$7,000,000 a $8,000,000", "value": 7000000},
                                        {"label": "$8,000,000 a $9,000,000", "value": 8000000},
                                        {"label": "$9,000,000 a $10,000,000", "value": 9000000},
                                        {"label": "Más de $10,000,000", "value": 10000000}
                                    ],
                                    value=400000,
                                    clearable=False,
                                    style={"width": "100%"},
                                ),
                            ],
                            size="lg",
                        ),
                        width=6,
                    ),
                ],
                justify="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="grafica_zonas"), width=10)
                ],
                justify="center",
            ),
        ],
        fluid=True,
        style={"backgroundColor": "#1a1a1a", "color": "white"},
    )


def register_callbacks(app):
    @app.callback(
        Output("grafica_zonas", "figure"),
        Input("dropdown_rango_presupuesto", "value")
    )
    def actualizar_grafica(rango_presupuesto):
        min_presupuesto, max_presupuesto = rango_presupuesto, rango_presupuesto + 1000000
        propiedades_en_rango = data[(data['Precios'] >= min_presupuesto) & (data['Precios'] <= max_presupuesto)]
        resultado = (
            propiedades_en_rango.groupby("Zona")["Precios"]
            .apply(lambda precios: len(precios))
            .reset_index()
            .rename(columns={"Precios": "PropiedadesComprables"})
        )

        if resultado.empty:
            fig = px.bar(title="No hay propiedades disponibles en este rango de presupuesto.")
        else:
            fig = px.bar(
                resultado,
                x="Zona",
                y="PropiedadesComprables",
                color="Zona",
                title=f"Propiedades Comprables en el rango de ${min_presupuesto} a ${max_presupuesto}",
                labels={"PropiedadesComprables": "Cantidad de Propiedades", "Zona": "Zona"},
                text_auto=True
            )
            fig.update_layout(template="plotly_dark", xaxis_title="Zona", yaxis_title="Propiedades Comprables")

        return fig
