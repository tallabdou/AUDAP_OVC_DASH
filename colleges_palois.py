import dash
import dash_html_components as html
import dash_table
import pandas as pd
from read_data_colleges_palois import df_colleges, gdf_colleges
from map_colleges_ut_palois import map_colleges_ut_palois

import dash_core_components as dcc
import dash_leaflet as dl

###################### prépartion tableau de données  ########################
df_colleges0 = df_colleges
df_colleges0 = df_colleges0.drop(df_colleges0.columns[[0, -1]], axis=1)
df_colleges0 = df_colleges0.sort_values(by=['libcommune'])
df_colleges0['ips_college'] = round(df_colleges0['ips_college'],2)
df_colleges0['ecart_type_ips_college'] = round(df_colleges0['ecart_type_ips_college'],2)

college_index = df_colleges.shape[0] - 4
col_name= {
    'libcommune': 'Commune',
    'libetab': 'Établissement',
    'ips_college': 'IPS collège',
    'ecart_type_ips_college': 'Ecart-type IPS',
    'nbr_collegiens': 'Nbr collégiens'
}

###################### prépartion carte des collèges  ########################
# Convertir la carte Folium en HTML
map_colleges_ut_palois_html = map_colleges_ut_palois().get_root().render()

########################  LAYOUT ####################


colleges_palois_layout =  html.Div([
    html.H1("Collèges Palois"),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col_name[col], 'id': col} for col in df_colleges0.columns],
        data=df_colleges0.to_dict('records'),
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '180px',
            'width': '180px',
            'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        style_data_conditional=[
            {'if': {'row_index': college_index}, 'backgroundColor': '#FF4136', 'color': 'white'},
        ]
    ),
    html.H1("Carte des collèges et UT avec IPS"),
    html.Iframe(srcDoc=map_colleges_ut_palois_html, style={'width': '100%', 'height': '100vh', 'margin': 'auto', 'display': 'block'}),
    html.Div(style={'height': '50px'}) 
], className='container')