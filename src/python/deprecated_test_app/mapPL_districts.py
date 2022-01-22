import dash
from dash import dcc
from dash import html
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

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
db = sqlalchemy.create_engine(
    config.DATABASE_ENGINE,
)
df_districts = pd.read_sql(
    "SELECT * FROM cases",
    db
)
with urlopen(config.PL_DISTRICTS_DIVISION_GEOJSON) as response:
    districts = json.load(response)

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
        id='map-PL_districts',
    )
])

covid_case_type = 'cases'


@app.callback(
    Output("map-PL_districts", "figure"),
    [Input("date-picker-single", "date")])
def choose_day(date_value):
    day = date.fromisoformat(date_value)

    fig_districts = px.choropleth(df_districts[df_districts.day == day], geojson=districts, locations='id_district',
                                  color=covid_case_type, color_continuous_scale="Reds",
                                  range_color=(0, 100),
                                  center={'lat': 52.54958385576375, 'lon': 19.68517500268937},
                                  labels=DTYPE_LABELS
                                  )

    fig_districts.update_geos(fitbounds="locations")
    fig_districts.update_geos(projection_type="orthographic")
    fig_districts.update_geos(
        visible=False,
        resolution=50, )
    return fig_districts


if __name__ == '__main__':
    app.run_server(debug=True, port=9999)
