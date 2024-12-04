import Portada as w
import Dashboard1 as das
import Dashboard2 as das2
import Dashboard3 as das3
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash, callback

app = Dash(external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return w.welcome()
    elif pathname == "/dash-1":
        return das.dashboard()
    elif pathname == "/dash-2":
        return das2.layout_dashboard()  # Llamar al layout del nuevo dashboard
    elif pathname == "/dash-3":
        return das3.create_layout()

def menu_dashboard():
    sidebar = html.Div(
        [
            html.H6("DashBoards", className="display-5", style={'color': 'white', 'fontSize': '43px'}),
            html.Hr(),
            html.P("Proyecto Final", className="lead", style={'color': 'white'}),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact", style={'color': 'white'}),
                    dbc.NavLink("Dashboard 1", href="/dash-1", active="exact", style={'color': 'white'}),
                    dbc.NavLink("Dashboard 2", href="/dash-2", active="exact", style={'color': 'white'}),
                    dbc.NavLink("Dashboard 3", href="/dash-3", active="exact", style={'color': 'white'}),
                    dbc.NavLink("Githbub", href="https://www.github.com", active="exact", target="_blank", style={'color': 'white'}),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="SIDEBAR_STYLE",
        style={'backgroundColor': 'black'}
    )

    content = html.Div(id="page-content", className="CONTENT_STYLE", style={'color': 'white'})

    return html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == "__main__":
    app.layout = menu_dashboard()
    das.register_callbacks(app)
    das2.register_callbacks(app)
    das3.register_callbacks(app)
    app.run(debug=True)
