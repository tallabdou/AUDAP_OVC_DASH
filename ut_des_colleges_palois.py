import dash
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
from dash import callback
from read_data_colleges_palois import df_ut, gdf_ut, df_ut0

import folium
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as colors

import dash_core_components as dcc
import dash_leaflet as dl

from map_ut_palois import f_map_ut_colleges_palois
###################### prépartion tableau de données  ########################
# df_ut0 = df_ut
# df_ut0 = df_ut0.drop(df_ut0.columns[[0, -1]], axis=1)
df_ut0 = df_ut0.drop(df_ut0.columns[[0]], axis=1)
df_ut0 = df_ut0.sort_values(by=['nom'])
df_ut0['ips_ut'] = round(df_ut0['ips_ut'],2)
df_ut0['ecart_type_ips_ut'] = round(df_ut0['ecart_type_ips_ut'],2)


col_name= {
    'nom': 'Nom UT',
    'ips_ut': 'IPS UT',
    'ecart_type_ips_ut': 'Ecart-type ips',
    'ips_nbr_collegiens': 'Nbr collégiens dans UT',
    'college_nom': 'Collège sectorisation'
}

###################### prépartion pour la carte folium ########################
m  = f_map_ut_colleges_palois(gdf_ut, 'ips_ut', 'nom_ut', 'ips_ut', 'ecart_type_ips_ut', 'ips_nbr_collegiens', 'college_nom')

# Convertir la carte Folium en HTML
map_html = m.get_root().render()

########################  LAYOUT ####################


ut_des_colleges_palois_layout =  html.Div([
    html.H1("UT"),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col_name[col], 'id': col} for col in df_ut0.columns],
        data=df_ut0.to_dict('records'),
        fixed_rows={'headers': True},
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
        },
        sort_action='native',
        style_cell={
            'height': 'auto',
            'minWidth': '180px',
            'width': '180px',
            'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
    ),
    html.Div(style={'height': '50px'}) ,
    html.H1("Carte des UT avec leurs IPS"),
    # Utiliser html.Iframe pour afficher la carte HTML
    # Ajoutez une liste déroulante pour sélectionner 'college_nom'
    dcc.Dropdown(
        id='college-dropdown',
        options=[{'label': col, 'value': col} for col in gdf_ut['college_nom'].unique()],
        value='',  # Valeur par défaut vide
        placeholder='Choisir un collège...',  # Texte d'invite
        clearable=False,
        style={'width': '400px'} 
    ),
    html.Div(style={'height': '30px'}),
    # Utiliser html.Iframe pour afficher la carte HTML
    html.Iframe(id='map-iframe', style={'width': '100%', 'height': '100vh', 'margin': 'auto', 'display': 'block'}),
    
    html.Div(style={'height': '50px'}) 
], className='container')


@callback(
    Output('map-iframe', 'srcDoc'),
    Input('college-dropdown', 'value')
)
def update_map(selected_college):
    if selected_college:
        # Filtrer les données en fonction de la sélection du collège
        filtered_gdf_ut = gdf_ut[gdf_ut['college_nom'] == selected_college]
    else:
        # Utiliser toutes les données si aucun collège n'est sélectionné
        filtered_gdf_ut = gdf_ut.copy()
    
    # Créez la carte mise à jour en fonction de la sélection
    m_updated = f_map_ut_colleges_palois(filtered_gdf_ut, 'ips_ut', 'nom_ut', 'ips_ut', 'ecart_type_ips_ut', 'ips_nbr_collegiens', 'college_nom')
    
    # Convertissez la carte Folium en HTML
    map_html_updated = m_updated.get_root().render()
    
    return map_html_updated