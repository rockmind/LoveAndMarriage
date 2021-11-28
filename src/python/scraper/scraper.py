import requests
import pandas as pd
from urllib.request import urlopen

data_path = 'https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data'

with urlopen(data_path) as f:
    html = f.read().decode('cp1250').encode('utf8')


r = requests.get(data_path)

print(r)