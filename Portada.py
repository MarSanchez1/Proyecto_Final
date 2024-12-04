from dash import  html

def welcome():
    body = html.Div(
        [
            html.H2("UNIVERSIDAD AUTÓNOMA DE BAJA CALIFORNIA", style={'textAlign': 'center', 'color': 'white'}),
            html.H3("FACULTAD DE CONTADURÍA Y ADMINISTRACIÓN", style={'textAlign': 'center', 'color': 'white'}),
            html.Img(
                src="https://comunicacioninstitucional.uabc.mx/wp-content/uploads/2024/03/escudo-actualizado-2022-w1000px-751x1024.png",
                width=300, height=300, style={'display': 'block', 'margin': 'auto'}
            ),
            html.Hr(),
            html.P("Análisis de Mercado Inmobiliario en México", style={'textAlign': 'center', 'color': 'white'}),
            html.P("Trabajo Final", style={'textAlign': 'left', 'color': 'white'}),
            html.H4("Integrantes", style={'textAlign': 'left', 'color': 'white'}),
            html.Ul(
                [
                    html.Li("Ahumada Lopez  Heber Alejandro"),
                    html.Li("Bernardino Sánchez julio Ezequiel"),
                    html.Li("Baca Lopez Jose Joaquin"),
                    html.Li("Castillo López Leslie Yareni"),
                    html.Li("Sanchez Muñoz Marisol"),
                ],
                style={'listStyleType': 'disc', 'paddingLeft': '10%', 'textAlign': 'left', 'color': 'white'}
            ),
            html.P("Docente: Josue Miguel Flores Parra", style={'textAlign': 'left', 'color': 'white'}),
            html.P("Curso: Programación para la Extracción de Datos ", style={'textAlign': 'left', 'color': 'white'}),
            html.P("Fecha: 03/12/2024", style={'textAlign': 'left', 'color': 'white'}),
            html.P("Grupo: 951 ", style={'textAlign': 'left', 'color': 'white'}),
        ],
        style={'backgroundColor': 'black'}
    )
    return body

