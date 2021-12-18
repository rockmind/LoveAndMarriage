import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy
from urllib.request import urlopen
from datetime import date
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

import src.config as config


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

db = sqlalchemy.create_engine(
    config.DATABASE_ENGINE,
)

with urlopen(config.PL_PROVINCES_DIVISION_GEOJSON) as response:
    provinces = json.load(response)

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
    df_provinces = pd.read_sql(
        "SELECT day, id_province, sum(cases) as cases, sum(deaths) as deaths, sum(recovered) as recovered FROM cases WHERE day = '{}' group by day, id_province".format(date_value),
        db
    )
    fig_provinces = px.choropleth(df_provinces, geojson=provinces, locations='id_province', color=covid_case_type,
                                  color_continuous_scale="PuRd",
                                  range_color=(df_provinces[covid_case_type].min(), df_provinces[covid_case_type].max()),
                                  center={'lat': 52.54958385576375, 'lon': 19.68517500268937},
                                  labels= DTYPE_LABELS
                                  )


    fig_provinces.update_geos(fitbounds="locations")
    fig_provinces.update_geos(projection_type="orthographic")
    fig_provinces.update_geos(
        visible=False,
        resolution=50, )
    return fig_provinces

if __name__ == '__main__':
    app.run_server(debug=True, port=9988)
