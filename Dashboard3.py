from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "19971995",
    "database": "INMOBILIARIA"
}

DATABASE_URI = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

engine = create_engine(DATABASE_URI)


APP_TITLE = "📊 Análisis de Mercado Inmobiliario Premium"

def clean_data():
    query = """
        SELECT 
            c.id_contenedor,
            z.nombre_zona AS Zona,
            ci.nombre_ciudad AS Ciudad,
            c.precios AS Precios,
            c.direcciones AS Direcciones,
            c.dimensiones AS Dimensiones
        FROM contenedora c
        JOIN zona z ON c.id_zona = z.id_zona
        JOIN ciudad ci ON c.id_ciudad = ci.id_ciudad;
    """
    try:
        df = pd.read_sql(query, engine)
        df['Precios'] = df['Precios'].astype(float)
        return df
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()

df = clean_data()

average_by_city = df.groupby("Zona")["Precios"].mean().reset_index()
average_by_city.rename(columns={"Precios": "Promedio de Precios"}, inplace=True)

def create_layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1(APP_TITLE, className="text-center text-light my-4"),
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Explora datos inmobiliarios, analiza precios y dimensiones por zonas YEI. ",
                        className="text-center text-secondary fs-5",
                    ),
                    width={"size": 8, "offset": 2},
                ),
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.RadioItems(
                            options=[
                                {"label": "Precios", "value": "Precios"},
                                {"label": "Dimensiones", "value": "Dimensiones"},
                            ],
                            value="Precios",
                            inline=True,
                            id="radio-buttons-final",
                            className="d-flex justify-content-center",
                        ),
                        width=12,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("📋 Datos Tabulares", className="text-light text-center my-3"),
                            dash_table.DataTable(
                                id="data-table",
                                data=df.to_dict("records"),
                                columns=[{"name": i, "id": i} for i in df.columns],
                                style_table={"overflowX": "auto"},
                                style_header={
                                    "backgroundColor": "#1c1e22",
                                    "fontWeight": "bold",
                                    "color": "#ffffff",
                                },
                                style_cell={
                                    "textAlign": "center",
                                    "backgroundColor": "#2a2d34",
                                    "color": "#ffffff",
                                    "border": "1px solid #2c2f36",
                                },
                                page_size=10,
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.H5("📈 Visualización de Datos", className="text-light text-center my-3"),
                            dcc.Graph(id="graph-final"),
                        ],
                        width=6,
                    ),
                ]
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.H5("🏙️ Promedio de Precios por Zona", className="text-light text-center my-3"),
                        dash_table.DataTable(
                            id="average-table",
                            data=average_by_city.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in average_by_city.columns],
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": "#1c1e22",
                                "fontWeight": "bold",
                                "color": "#ffffff",
                            },
                            style_cell={
                                "textAlign": "center",
                                "backgroundColor": "#2a2d34",
                                "color": "#ffffff",
                                "border": "1px solid #2c2f36",
                            },
                            page_size=5,
                        ),
                    ],
                    width={"size": 8, "offset": 2},
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Análisis visual Y intuitivo.",
                        className="text-center text-secondary my-4",
                    ),
                    width=12,
                )
            ),
        ],
        fluid=True,
    )

def register_callbacks(app):
    @app.callback(
        Output("graph-final", "figure"),
        Input("radio-buttons-final", "value"),
    )
    def update_graph(column_chosen):
        fig = px.bar(
            df,
            x="Zona",
            y=column_chosen,
            color="Zona",
            text_auto=True,
            title=f"Promedio de {column_chosen} por Zona",
            labels={"Zona": "Zona", column_chosen: f"Promedio de {column_chosen}"},
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig.update_layout(
            template="plotly_dark",
            title_font_size=22,
            title_font_color="#00c0ff",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
        )
        return fig

def create_app():
    external_stylesheets = [dbc.themes.SOLAR]
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.title = APP_TITLE
    app.layout = create_layout()
    register_callbacks(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
