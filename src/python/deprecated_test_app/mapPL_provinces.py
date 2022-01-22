from asyncio import run

import dash
from dash import dcc
from dash import html
from urllib.request import urlopen
from datetime import date
import plotly.express as px
import json
from dash.dependencies import Input, Output

import src.config as config
from python.services import LoveAndMarriageDB


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


df_provinces = run(LoveAndMarriageDB.get_provinces())

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
    day = date.fromisoformat(date_value)
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
