from asyncio import get_event_loop

import dash
import plotly.express as px
import pandas as pd
from dash import dcc
from dash import html
from datetime import date, datetime
from dash.dependencies import Input, Output

from front_config import DTYPE_LABELS
from services import json_loads
from services.rpc_services import covid_db_api


app = dash.Dash(__name__, requests_pathname_prefix='/provinces/')


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def get_provinces():

    results = get_event_loop().run_until_complete(covid_db_api.rpc_request([
        'get_provinces_cases',
        'get_provinces_geojson'
    ]))

    df = pd.read_json(results[0]['result'], convert_dates=['date'])

    return df, json_loads(results[1]['result'])


df_provinces, geo_provinces = get_provinces()


app.layout = html.Div([
    html.H1(children='koronawirus w Polsce'),
    dcc.DatePickerSingle(
        id='date-picker-single',
        min_date_allowed=date(2020, 11, 24),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        date=date.today()
    ),
    html.Div(id='output-container-date-picker-single'),
    dcc.Graph(
        id='map-PL_provinces',
    )
])

covid_case_type = 'cases'


@app.callback(
    Output("map-PL_provinces", "figure"),
    [Input("date-picker-single", "date")])
def choose_day(date_value):
    day = datetime.fromisoformat(date_value)
    fig_provinces = px.choropleth(df_provinces[df_provinces.date == day], geojson=geo_provinces,
                                  locations='id_province', color=covid_case_type,
                                  color_continuous_scale="Reds",
                                  range_color=(0, 1000),
                                  center={'lat': 52.54958385576375, 'lon': 19.68517500268937},
                                  labels=DTYPE_LABELS
                                  )
    fig_provinces.update_geos(fitbounds="locations")
    fig_provinces.update_geos(projection_type="orthographic")
    fig_provinces.update_geos(
        visible=False,
        resolution=50, )
    return fig_provinces

