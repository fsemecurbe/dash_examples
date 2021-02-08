import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import igraph






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

 dcc.Dropdown(
        id='my-input',
        options=[{'label': 'France', 'value': 'FRA'}, {'label': 'Germany', 'value':'DEU'}],
        value='FRA'
    ),
   
    html.Div(id='my-output'),
    html.Div([
    html.Div([dcc.Graph(id='map_ex'),], className='six columns'),
    html.Div([dcc.Graph(id='map_im'),], className='six columns')
    ], className='row')          
             
])


@app.callback(Output('my-output', 'children'),
              Output('map_ex', 'figure'),
              Output('map_im', 'figure'),
              Input('my-input', 'value'))
    
def update_output_div(input_value):
    
    return ('Output: {}'.format(input_value),
            px.scatter_geo(flow[flow.j_country==input_value], locations="i_country", size="v", projection="natural earth"),
            px.scatter_geo(flow[flow.i_country==input_value], locations="j_country", size="v", projection="natural earth"))

if __name__ == '__main__':
    app.run_server(debug=True)
