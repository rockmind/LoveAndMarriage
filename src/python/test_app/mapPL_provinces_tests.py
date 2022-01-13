from asyncio import run

import dash
import requests
from dash import dcc
from dash import html
from urllib.request import urlopen
from datetime import date, datetime
import plotly.express as px
import json
import pandas as pd
from dash.dependencies import Input, Output
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

import src.config as config
from python.services import LoveAndMarriageDB
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CASES = 'cases'
DEATHS = 'deaths'
RECOVERED = 'recovered'
CASES_PL = 'Liczba przypadków'
DEATHS_PL = 'Liczba zgonów'
RECOVERED_PL = 'Liczba_ozdrowieńców'
DTYPE_LABELS = {CASES: CASES_PL, DEATHS: DEATHS_PL, RECOVERED: RECOVERED_PL}
DATA_TYPE_COLORS = {CASES: "red", DEATHS: "black", RECOVERED: "green"}

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def get_token():
    username = 'johndoe'
    password = 'FoolishPassword'

    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=username))
    token = oauth.fetch_token(token_url='http://127.0.0.1:8888/token/', username=username, password=password)
    return token


token = get_token()


def get_provinces():
    BASE_URL = 'http://127.0.0.1:8888/provinces/'
    headers = {
        'Authorization': f'{token["token_type"]} {token["access_token"]}',
        'Content-Type': 'application/json'
    }
    auth_response = requests.get(BASE_URL, headers=headers)
    df = pd.read_json(auth_response.json(), convert_dates=['day'])

    return df


df_provinces = get_provinces()


with urlopen(config.PL_PROVINCES_DIVISION_GEOJSON) as response:
    geo_provinces = json.load(response)

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
    fig_provinces = px.choropleth(df_provinces[df_provinces.day == day], geojson=geo_provinces,
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


if __name__ == '__main__':
    app.run_server(debug=True, port=9988)
