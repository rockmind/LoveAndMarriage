import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import config

import pandas as pd
from asyncio import run
from services.rpc_services import covid_db_api

CASES = config.CASES
DEATHS = config.DEATHS
RECOVERED = config.RECOVERED
CASES_PL = config.PL_CASES
DEATHS_PL = config.PL_DEATHS
RECOVERED_PL = config.PL_RECOVERED
DATA_TYPE_COLORS = {CASES: "red", DEATHS: "black", RECOVERED: "green"}


app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


# db = sqlalchemy.create_engine(
#     config.DATABASE_ENGINE,
# )
# df = pd.read_sql(
#     """select day, sum(cases.cases) as cases, sum(deaths) as deaths, sum(recovered) as recovered
#        from cases
#        group by day
#        order by day desc""",
#     db
# )
def get_cases():

    results = run(covid_db_api.rpc_request([
        'get_all_cases'
    ]))

    df = pd.read_json(results[0]['result'], convert_dates=['date'])

    return df


df = get_cases()


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
        data=go.Bar(x=df.date, y=df[data_type], marker_color=DATA_TYPE_COLORS[data_type]))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=9997)
