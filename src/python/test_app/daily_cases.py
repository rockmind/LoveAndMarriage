import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import src.config as config

CASES = config.CASES
DEATHS = config.DEATHS
RECOVERED = config.RECOVERED
CASES_PL = config.PL_CASES
DEATHS_PL = config.PL_DEATHS
RECOVERED_PL = config.PL_RECOVERED
DATA_TYPE_COLORS = {CASES:"red", DEATHS:"black", RECOVERED:"green"}


app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


db = sqlalchemy.create_engine(
    config.DATABASE_ENGINE,
)
df = pd.read_sql(
    """select day, sum(cases.cases) as cases, sum(deaths) as deaths, sum(recovered) as recovered
       from cases
       group by day
       order by day desc""",
    db
)

app.layout = html.Div([
    html.H1(children='koronawirus w Polsce'),
    dcc.Dropdown(id="dropdown",
                 options=[
                     {'label': k, 'value': v}
                     for k, v in {CASES_PL:CASES, DEATHS_PL:DEATHS, RECOVERED_PL:RECOVERED}.items()
                 ],
                 value=CASES,
                 clearable=False,
                 ),
    dcc.Graph(
        id='daily-cases',
    )
])

@app.callback(
    Output("daily-cases", "figure"),
    [Input("dropdown", "value")])
def choose_data(data_type):
    fig = go.Figure(
        data=go.Bar(x=df.day, y=df[data_type], marker_color=DATA_TYPE_COLORS[data_type]))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)