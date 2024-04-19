#import the necessary libraries
import dash
from dash import Dash, html, dcc, callback # we are adding one more component to be able to add the graphs/tables
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from sqlalchemy import create_engine
from sqlalchemy import text  # to be able to pass string
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PW')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')

url = f'postgresql://{username}:{password}@{host}:{port}/climate'

engine = create_engine(url)

with engine.begin() as conn: 
    result = conn.execute(text("SELECT * FROM mart_forecast_day;")) 
    data = result.all() # also you can use fetchall.

with engine.begin() as conn: 
    result = conn.execute(text("SELECT * FROM mart_conditions_week;")) 
    data2 = result.all() # also you can use fetchall.
data2


#prepare the visualisations you will use
##read the data and filter if necessary

df = pd.DataFrame(data) 
df2 = pd.DataFrame(data2)
mask1 = ['city','avg_temp_c','max_temp_c','min_temp_c','date']
mask_weather_condition = ['city', 'month_of_year', 'sunny_days', 'rainy_days', 'mystical_days', 'snow_days', 'cloudy_days', 'stay_at_home_days']
weather_condition = df2[mask_weather_condition]
df_mask1 = df[mask1]
wind = ['city', 'month_of_year', 'max_wind_kph']
wind_df = df[wind]
wind_wind = wind_df.groupby(['month_of_year', 'city']).mean().reset_index()
wind_wind = pd.DataFrame(wind_wind)
graph = dcc.Graph()
cities =df_mask1['city'].unique().tolist() 
image_path1 = 'assets/stornoway_image_small.jpg'
image_path2 = 'assets/portree_image_small.jpg'
image_path3 = 'assets/glasgow_image_small.jpg'

'''table_updated2 = dash_table.DataTable(df[mask1].to_dict('records'),
                                  [{"name": i, "id": i} for i in df[mask1].columns],
                               style_data={'color': 'white','backgroundColor': 'black', 'textAlign': 'center'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold', 'textAlign': 'center'}, 
                                     style_table={
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px', 
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                     'marginTop': 0, 'marginBottom': 0} 
                                     )
'''
fig_null = px.scatter_mapbox(
                        data_frame=df2,
                        lat='lat', 
                        lon='lon', 
                        hover_name='city', 
                        color='city',
                        
                        # start location and zoom level
                        zoom=4, 
                        center={'lat': 55.86, 'lon': -4.25},
                        title = 'Cities on Map', 
                        mapbox_style='open-street-map'
                       )
fig_null = fig_null.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", )
graph_null = dcc.Graph(figure=fig_null)

fig_sunny = px.bar(weather_condition, x='month_of_year', y='sunny_days', barmode='group', color='city', title="Sunny Days :(")
fig_sunny = fig_sunny.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white")
graph_sunny = dcc.Graph(figure=fig_sunny)

fig_rainy = px.bar(weather_condition, x='month_of_year', y='rainy_days', barmode='group', color='city', title="Rainy Days :'(")
fig_rainy = fig_rainy.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white")
graph_rainy = dcc.Graph(figure=fig_rainy)

fig1 = px.bar(df_mask1, title='Average Temprature - Bar Plot', x='date', y='avg_temp_c', height=300, color='city')
fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph1 = dcc.Graph(figure=fig1)

fig2 = px.line(data_frame=df_mask1, x='date', y='avg_temp_c', title="Average Temperature per City - Line Plot", markers=True, color='city')
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)

fig3 = px.line(data_frame=df_mask1, x='date', y='max_temp_c', title="Maximum Temperature per City - Line Plot", markers=True, color='city')
fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
graph3 = dcc.Graph(figure=fig3)

fig4 = px.line(data_frame=df_mask1, x='date', y='min_temp_c', title="Minimum Temperature per City - Line Plot", markers=True, color='city')
fig4 = fig4.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
graph4 = dcc.Graph(figure=fig4)

fig_windy = px.line(wind_wind, x='month_of_year', y='max_wind_kph', title='Max Wind km/h per City', markers=True, color='city')
fig_windy = fig_windy.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
graph_windy = dcc.Graph(figure=fig_windy)

#the app

app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# NOW ADDING THE SERVER

server = app.server

dropdown = dcc.Dropdown(['Glasgow', 'Stornoway', 'Portree '], 
                        value=['Glasgow', 'Stornoway', 'Portree '], 
                        clearable=False, 
                        multi=True, 
                        style={'paddingLeft': '30px', 
                               "backgroundColor": "#222222", 
                               "color": "#222222"})
#we added the styling to the dropdown menu

app.layout = html.Div(children=[html.H1("Huseyin's First Dash, Weather Conditions Analysis (Apr 2023 to Apr 2024) for 3 Selected Locations in Scotland: Glasgow, Stornoway, Portree", 
                                style={'textAlign': 'center', 'color': '#636EFA'}), 

                        html.Div(children=html.P("What is the goal? Investigating 3 parts of Scotland based on the following: More sunny days, Less rainy days, Low wind km/h, Higher avg tempratures per week, month, per season, and especially during summer period"), 
                                style={'textAlign': 'center', 'color': '#636EFA',
                                       'marginLeft': 'auto', 'marginRight': 'auto', 'marginBottom': '20px'}),
                        
                        html.Div(children=html.P("Selected Locations View"), 
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),
                                graph_null,

                        html.Div(children=html.P("How Stornoway looks like?"),
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),
                                        
                        html.Div(children=html.Img(src=image_path1),
                                 style={'width': '900px', 'margin': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),

                        html.Div(children=html.P("How about Portree?"),
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),

                        html.Div(children=html.Img(src=image_path2),
                                style={'width': '900px', 'margin': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),

                        html.Div(children=html.P("And finally Glasgow? Note: Picture is taken by me :)"),
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),

                        html.Div(children=html.Img(src=image_path3),
                                style={'width': '900px', 'margin': 'auto', 'textAlign': 'center', 'marginBottom': '50px'}),

                        html.Div(children=html.P("Sunny vs Rainy Days Comparison"), 
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),
                                graph_sunny, graph_rainy,

                        html.Div(children=html.P("Temperature - Bar Plot View"), 
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),
                                graph1,

                        html.Div(children=[html.Div('Temperature - Line Plot View', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white','width': '33%',
                                                 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),   
                                dropdown, graph2, graph3, graph4]),

                        html.Div(children=html.P("Wind Comparison"), 
                                style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center', 'marginBottom': '20px'}),
                                graph_windy,

                        html.Div(children=html.P("Result: Maybe I should reconsider my off grid plan locations?"), 
                                style={'textAlign': 'center', 'color': '#636EFA',
                                       'marginLeft': 'auto', 'marginRight': 'auto', 'marginBottom': '20px'}),


])

@callback(
    [Output(graph2, "figure"), Output(graph3, "figure"), Output(graph4, "figure")], 
    Input(dropdown, "value"))

#Output(component_id='my-output', component_property='children'),
#Input(component_id='my-input', component_property='value')

def update_bar_chart(cities): 

    mask = df_mask1["city"].isin(cities) # coming from the function parameter
    fig2 =px.line(df_mask1[mask], 
             x='date', 
             y='avg_temp_c',
             color= 'city',
             color_discrete_map = {'Glasgow': '#7FD4C1', 'Stornoway': '#8690FF', 'Portree ': '#F7C0BB'},
             title = f"{cities} Average Temperature",)
    fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white")

    fig3 =px.line(df_mask1[mask], 
             x='date', 
             y='max_temp_c',
             color= 'city',
             color_discrete_map = {'Glasgow': '#7FD4C1', 'Stornoway': '#8690FF', 'Portree ': '#F7C0BB'},
             title = f"{cities} Max Temperature",)
    fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white")

    fig4 =px.line(df_mask1[mask], 
             x='date', 
             y='min_temp_c',
             color= 'city',
             color_discrete_map = {'Glasgow': '#7FD4C1', 'Stornoway': '#8690FF', 'Portree ': '#F7C0BB'},
             title = f"{cities} Min Temperature",)
    fig4 = fig4.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

    return fig2, fig3, fig4 # whatever you are returning here is connected to the component property of
                       #the output which is figure

if __name__ == '__main__':
     app.run_server(debug=True) # put debug=True to run the changes immediately