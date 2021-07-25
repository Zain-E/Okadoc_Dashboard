
#================================================= IMPORT LIBRARIES ====================================================

import pandas as pd
import plotly.express as px
import boto3
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import base64
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import io
import xlrd
import numpy
import openpyxl

#================================================= AWS S3 CONNECTION ===================================================

access_key_ID ='AKIAXSF52DIAIYVY3EOU'
secret_access_key ='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'
bucket_name = 'zainprojects'
upload_file_key = 'COVID_Analysis/Excel_Documents/'



s3 = boto3.client('s3', aws_access_key_id=access_key_ID, aws_secret_access_key=secret_access_key)


#Reads the files in the S3 repo so we can use as a df

# UAE Covid data
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}UAE_COVID_Data.xlsx')
data = obj['Body'].read()
UAE_Covid_data = pd.read_excel(io.BytesIO(data))

# Multiple Country Covid data
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}MultipleCountries_COVID_Data_v3.xlsx')
data = obj['Body'].read()
All_Covid_data = pd.read_excel(io.BytesIO(data))

#=============================================== DATA MANIPULATION =====================================================

# Country Drop down
Country_list = All_Covid_data['location'].unique()
print(Country_list)

# Metric Drop down
Metric_list = All_Covid_data['Measure'].unique()
print(Metric_list)

#================================================ DASHBOARD LAYOUT =====================================================


app = dash.Dash(__name__, eager_loading=True, external_stylesheets=[dbc.themes.LUX])
server = app.server
image_filename = r'assets\Okadoc-Logo.png' # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename = r'assets\GitHub.png' # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
encoded_image_Git = base64.b64encode(open(image_filename, 'rb').read())
image_filename_ONS = r'assets\ONS.png' # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
encoded_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())

app.layout = html.Div([
                        dbc.Row([
                                #dbc.Col(html.H1('COVID-19 Activity Dashboard',className='dark'),style={'text-align': 'center','vertical-align':'middle'}),
                                dbc.Col(html.A(href='https://www.okadoc.com/en-ae/', children=html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width=130, height=130, style={'vertical-align':'middle'}),target="_blank"), width={'size': 12, 'offset':0}),
                                ],style={'text-align': 'center'}),

                        dbc.Row([
                                dbc.Col(html.H4('COVID-19 Activity Dashboard',className='dark'),style={'text-align': 'center','vertical-align':'middle'}),
                            ]),

                        html.Hr(),

                       dcc.Tabs(id="tabs", value='region-tab', children=[

                                # TAB 1 - COVID CASES
                                dcc.Tab(label='Region', value='region-tab', children=[html.Div([

                                    html.Hr(),

                                    dbc.Row([
                                       # dbc.Col(children=html.Img(id='flag', width=65, height=35, style={'vertical-align': 'top'}), width={'size': 1, 'offset': 1}),

                                        dbc.Col(dcc.Dropdown(id='country_dropdown',
                                                                  options=[
                                                                      {"label": Country_list[0],
                                                                       "value": Country_list[0]},
                                                                      {"label": Country_list[1],
                                                                       "value": Country_list[1]},
                                                                      {"label": Country_list[2],
                                                                       "value": Country_list[2]},
                                                                      {"label": Country_list[3],
                                                                       "value": Country_list[3]},
                                                                      {"label": Country_list[4],
                                                                       "value": Country_list[4]},
                                                                      {"label": Country_list[5],
                                                                       "value": Country_list[5]},
                                                                      {"label": Country_list[6],
                                                                       "value": Country_list[6]}
                                                                  ],
                                                                  multi=False,
                                                                  value=Country_list[5],
                                                                  style={'text-align': 'center'},
                                                                  clearable=False,
                                                                  placeholder='Please select Country'
                                                                  ), width={'size': 5, 'offset': 1}),

                                    dbc.Col(dcc.Dropdown(id='metric_dropdown',
                                                                  options=[
                                                                      {"label": Metric_list[0],
                                                                       "value": Metric_list[0]},
                                                                      {"label": Metric_list[1],
                                                                       "value": Metric_list[1]},
                                                                      {"label": Metric_list[2],
                                                                       "value": Metric_list[2]},
                                                                      {"label": Metric_list[3],
                                                                       "value": Metric_list[3]},
                                                                      {"label": Metric_list[4],
                                                                       "value": Metric_list[4]},
                                                                      {"label": Metric_list[6],
                                                                       "value": Metric_list[6]},

                                                                  ],
                                                                  multi=False,
                                                                  value=Metric_list[1],
                                                                  style={'text-align': 'center'},
                                                                  clearable=False,
                                                                  placeholder='Please select a metric'
                                                                  ), width={'size': 5, 'offset': -1})


                                             ]),

                                    html.Hr(),

                                    # dbc.Row(
                                    #     dbc.Col(html.H3('Statistics', style={'text-align': 'center'}))),

                                    dbc.Row(dbc.Col(children=html.Img(id='flag', width=65, height=35, style={'vertical-align': 'top','text-align': 'center'}), width={'size': 12}), style={'text-align': 'center'}),

                                    dbc.Row([dbc.Col(dcc.Graph(id='Graph 0', figure={}), width={'size': 10, 'offset': 1})]),

                                    html.Hr(),
                                    html.Br(),

                                    dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([html.H3("Total cases", className="card-title",style={'text-align': 'center'}),html.H2(id='COVID cases',style={'text-align': 'center'},className="card-text")]),color="info",outline=True),width={'size': 3, 'offset': 1}),
                                             dbc.Col(dbc.Card(dbc.CardBody([html.H3("Total deaths",className="card-title",style={'text-align': 'center'}),html.H2(id='COVID deaths',style={'text-align': 'center'},className="card-text")]),color="info",outline=True), width={'size': 2}),
                                             dbc.Col(dbc.Card(dbc.CardBody([html.H3("Population",className="card-title",style={'text-align': 'center'}),html.H2(id='Population',style={'text-align': 'center'},className="card-text")]),color="info", outline=True),width={'size': 2}),
                                             dbc.Col(dbc.Card(dbc.CardBody([html.H3("Total Tests",className="card-title",style={'text-align': 'center'}),html.H2(id='Tests',style={'text-align': 'center'},className="card-text")]),color="info", outline=True),width={'size': 3, 'offset': -1}),
                                             ]),

                                    html.Hr(),
                                    html.Br(),
                                    html.Br(),

                                    dbc.Row([dbc.Col(html.H1(id='Card',style={'text-align': 'center', 'fontColor':'red'}, className="card-text"),width={'size': 10, 'offset': 1})
                                             ]),

                                    html.Br(),

                                    dbc.Row([dbc.Col(html.H3(f'Download the Okadoc App',style={'text-align': 'center'}), width={'size': 10, 'offset': 1}),
                                             dbc.Col(html.H6('Instantly find a practitioner across 16,000+ profiles, 140 specialities in 1600+ clinics and hospitals all over UAE', style={'text-align': 'center'}),width={'size': 10, 'offset': 1})

                                             ]),

                                    html.Br(),
                                    html.Hr(),

                                ])]),

                               # TAB 4 - MAP
                                dcc.Tab(label='Map', value='rec-tab', children=[

                                   html.Hr(),

                                   # dbc.Row(dbc.Col(html.H3('Total Cases & Deaths', style={'text-align': 'center'}),
                                   #                 width={'size': 10, 'offset': 1})),
                                   html.Br(),
                                   html.Br(),

                                    dbc.Row([dbc.Col(dcc.Graph(id='Map', figure={}), width={'size': 10, 'offset': 1})]),

                                    html.Br(),
                                    html.Br(),
                                    html.Hr(),

                                    dbc.Row([
                                             dbc.Col(html.A(href='https://github.com/CSSEGISandData/COVID-19', children='This app was powered by Heroku and Amazon Web Services.  Data obtained from JHU CSSE COVID-19 Data',target="_blank"), width={'size': 10, 'offset': 1})
                                             ],style={'text-align': 'center'}),

                                    html.Hr(),

                                    dbc.Row([
                                        dbc.Col(html.A(href='https://github.com/Zain-E/BARTS_COVID_Dashboard',
                                                       children=html.Img(src='data:image/png;base64,{}'.format(
                                                           encoded_image_Git.decode()), width=60, height=60,
                                                           style={'vertical-align': 'middle'}),
                                                       target="_blank"), width={'size': 1, 'offset': -1}),
                                        dbc.Col(html.A(
                                            href='https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsduetocovid19bylocalareaanddeprivation',
                                            children=html.Img(
                                                src='data:image/png;base64,{}'.format(encoded_image_ONS.decode()),
                                                width=60, height=60, style={'vertical-align': 'middle'}),
                                            target="_blank"), width={'size': 1, 'offset': -2})

                                    ]),

                                ]),
                        ])

])
#============================================= GRAPH 0 =================================================================

@app.callback(Output('Graph 0', 'figure'),

              [Input(component_id='country_dropdown', component_property='value'),
               Input(component_id='metric_dropdown', component_property='value')]
              )

def render_content(country,metric):

    df = All_Covid_data.copy()
    df = df[df['location']==country]
    df = df[df['Measure']==metric]


    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df["date"], y=df["Activity"], name=metric,
                   line=dict(color='royalblue', width=4),fill='tozeroy'))

    #fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y", title='')

    fig.update_xaxes(showgrid=True,
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(step="all"),
                dict(count=10, label="10m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward")
            ])
        )
    )

    fig.update_yaxes(showgrid=True)

    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    #'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },
    title={
    'text': metric + ' - ' + country,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'
    })


    return fig

#=============================================  CARDS  =================================================================

@app.callback([Output('COVID cases', 'children'),
               Output('Population', 'children'),
               Output('COVID deaths', 'children'),
               Output('Tests', 'children')],

              [Input(component_id='country_dropdown', component_property='value')]
              )

def render_content(country):

    df = All_Covid_data.copy()
    df = df[df['location']==country]

    # Card Metrics
    most_recent_date = All_Covid_data['date'].max()

    df_cases = df[df['Measure']=='Total Cases']
    df_cases = df_cases[df_cases['date']==most_recent_date]
    cases=df_cases['Activity']
    cases = f'{int(cases):,}'

    df_population = df[df['Measure']=='Population']
    df_population = df_population[df_population['date']==most_recent_date]
    df_population=df_population['Activity']
    pop = f'{int(df_population):,}'

    df_deaths = df[df['Measure']=='Total Deaths']
    df_deaths = df_deaths[df_deaths['date']==most_recent_date]
    death=df_deaths['Activity']
    death = f'{int(death):,}'

    df_tests = df[df['Measure']=='Total Tests']
    df_tests = df_tests[df_tests['date']==most_recent_date]
    tests=df_tests['Activity']
    try:
        tests = f'{int(tests):,}'
    except:
        tests = 'N/A'

    return cases,pop,death,tests

#============================================= FLAG IMAGES =============================================================

@app.callback(Output('flag', 'src'),

              [Input(component_id='country_dropdown', component_property='value')]
              )

def render_content(country):

    image_filename_ONS = r'assets\UAE.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    UAE_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())
    image_filename_ONS = r'assets\Saudi.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    Saudi_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())
    image_filename_ONS = r'assets\Bahrain.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    Bahrain_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())
    image_filename_ONS = r'assets\Kuwait.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    Kuwait_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())
    image_filename_ONS = r'assets\Oman.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    Oman_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())
    image_filename_ONS = r'assets\Qatar.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    Qatar_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())
    image_filename_ONS = r'assets\Yemen.png'  # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
    Yemen_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())

    if country == Country_list[0]:
         src = 'data:image/png;base64,{}'.format(Bahrain_image_ONS.decode())
    elif country == Country_list[1]:
         src = 'data:image/png;base64,{}'.format(Kuwait_image_ONS.decode())
    elif country == Country_list[2]:
         src = 'data:image/png;base64,{}'.format(Oman_image_ONS.decode())
    elif country == Country_list[3]:
         src = 'data:image/png;base64,{}'.format(Qatar_image_ONS.decode())
    elif country == Country_list[4]:
         src = 'data:image/png;base64,{}'.format(Saudi_image_ONS.decode())
    elif country == Country_list[5]:
        src = 'data:image/png;base64,{}'.format(UAE_image_ONS.decode())
    elif country == Country_list[6]:
        src = 'data:image/png;base64,{}'.format(Yemen_image_ONS.decode())
    else:
        print('N/A')

    return src


#============================================= GRAPH MAP ===============================================================


access_token = 'pk.eyJ1IjoiemFpbmVpc2EiLCJhIjoiY2tlZWg0MXJvMGcwZzJyb3k1OXh0Ym55aiJ9.0SJ_VBRVxyWd6SmbdUwmKQ'

@app.callback(Output('Map', 'figure'),

               Input(component_id='country_dropdown', component_property='value'))


def render_content(country):

        df = All_Covid_data.copy()
        #df = df[df['location'] == country]
        df = df[df['Measure']=='Total Cases']

        # Card Metrics
        most_recent_date = All_Covid_data['date'].max()
        df = df[df['date'] == most_recent_date]

    # REMEMBER the as_index function turns the aggregate output from a Series into a Dataframe - important as some graphs/figures need Dfs
    #     dfmap_group = df_merged.groupby(['Area of usual residence name', 'Lat', 'Long'], as_index=False)['Deaths'].sum()
        df['Cases for label'] = df['Activity'].map('{:,.0f}'.format)
        df['Label'] = df['Cases for label'].astype(str) + ' cases in ' + df['location']

        locations = [go.Scattermapbox(
            lon=df['Lon'],
            lat=df['Lat'],
            mode='markers',
            unselected={'marker': {'opacity': 0.5}},
            selected={'marker': {'opacity': 1, 'size': 50}},
            hoverinfo='text',
            hovertext=df['Label'],
            marker=dict(
                size=df['Activity'] / 100,
                color='blue',
                sizemode='area'
            )
        )]

        return {
                    'data': locations,
                    'layout': go.Layout(
                        uirevision='foo',  # preserves state of figure/map after callback activated
                        clickmode='event+select',
                        margin=dict(l=0, r=0, t=0, b=0),
                        hovermode='closest',
                        hoverdistance=2,
                        #title=dict(text="COVID CASES MAPPED", font = dict(size=35)), #irrelevant with the margins given
                        mapbox=dict(
                            accesstoken=access_token,
                            bearing=25,
                            # style='dark', # Can enter to style the graph
                            center=dict(
                                lat=22.31479017650484,
                                # 51.50853, # is technically the centre of London, but the other co-ordinates fit better
                                lon=51.71945191684147
                                # -0.12574 # is technically the centre of London, but the other co-ordinates fit better
                            ),
                            pitch=20,
                            zoom=5
                        ),
                    )
                }



#=======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True)
