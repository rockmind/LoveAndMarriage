import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from starlette.middleware.wsgi import WSGIMiddleware


token_auth_scheme = HTTPBearer()

server = FastAPI()

app = dash.Dash(__name__, requests_pathname_prefix="/dash/")

app.layout = html.Div([
    html.P("Color:"),
    dcc.Dropdown(
        id="dropdown",
        options=[
            {'label': x, 'value': x}
            for x in ['Gold', 'MediumTurquoise', 'LightGreen']
        ],
        value='Gold',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    [Input("dropdown", "value")])
def display_color(color):
    fig = go.Figure(
        data=go.Bar(y=[2, 3, 1], marker_color=color))
    return fig


@server.get("/dash", response_class=HTMLResponse)
def my_dash_app():
    return app.index()


@server.get("/")
async def root():
    return {"message": "Hello World"}


@server.get("/api/private")
def private(token=Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""

    result = token.credentials

    return result


if __name__ == "__main__":
    # app.run_server(debug=True)
    server.mount("/dash", WSGIMiddleware(app.server))
    # uvicorn.run(server, host="0.0.0.0", port=8000)
    uvicorn.run(server, port=8888)
