import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

#load data
flow = pd.read_csv('data/trade_2018.csv')
codes = pd.read_csv('shapefiles/country_codes_V202001.csv', engine='python')
flow = flow.merge(codes[['country_code', 'iso_3digit_alpha']], left_on='i', right_on='country_code')
flow = flow.merge(codes[['country_code', 'iso_3digit_alpha']], left_on='j', right_on='country_code')
flow = flow.rename(columns={'iso_3digit_alpha_x': 'i_country', 'iso_3digit_alpha_y': 'j_country'})
flow = flow[['i_country', 'j_country', 'v', 'q']]

available_indicators = flow['i_country'].unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
   # html.Div(["Input: ",
   #           dcc.Input(id='my-input', value=available_indicators[0], type='text')]),
 dcc.Dropdown(
        id='my-input',
        #options=[{'label': i, 'value': i} for i in available_indicators[:20]],
        options=[{'label': 'France', 'value': 'FRA'}, {'label': 'Germany', 'value':'DEU'}],
        value='FRA'
    ),
    html.Div(id='my-output')
])


@app.callback(Output('my-output', 'children'),
              Input('my-input', 'value'))
    
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
