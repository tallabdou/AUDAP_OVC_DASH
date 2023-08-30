import dash
import dash_core_components as dcc
from dash import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
from read_data import df
from dash.dependencies import Input, Output, State
from dash import callback
import pandas as pd
import numpy as np

# Définir le layout de l'application
ut_layout = html.Div([
    html.H1("Unité territoriale"),
    dcc.Dropdown(
        id='index-value-dropdown-ut',
        options=[{'label': str(val), 'value': str(val)} for val in df.nom_ut.unique()],
        value=str(df.nom_ut.unique()[0]),
        clearable=False,
        style={'width': '50%'} 
    ),
    html.Div(id='table-body-ut', className='table-responsive', style={'marginTop': 20}),
    html.Div(id='effectif-total-ut', style={'marginTop': 20})
    ], className='container')


@callback(
    [Output('table-body-ut', 'children'),
     Output('effectif-total-ut', 'children')],
    Input('index-value-dropdown-ut', 'value'))
def update_table(index_value):
    df_filtered = df.loc[df['nom_ut'] == index_value]
    table = pd.pivot_table(df_filtered, values='num', index=['libetab'], columns='libpcs', aggfunc=len)
    col_sum = table.sum(axis=0, skipna=True)

    selected_rows = table.reset_index()
    selected_rows = selected_rows.sort_values(by=['libetab'])
    
    # # Ajouter la somme des colonnes à la dernière ligne avec 'Total' dans la première colonne
    new_row_dict = {selected_rows.columns[0]: 'Total colonne'}
    for i, col_name in enumerate(selected_rows.columns[1:]):
        new_row_dict[col_name] = col_sum.iloc[i]
    new_row = pd.DataFrame(new_row_dict, index=[0])
    
    df_f = pd.concat([selected_rows, new_row], ignore_index=True)

    # Liste des colonnes à réordonner
    col_order = ['libetab', 'Cadres supérieurs et enseignants', 'Cadres moyens', 'Employés, artisans, commerçants et agriculteurs', 'Ouvriers et inactifs', 'Non renseignée']
    df_f = df_f.reindex(columns=col_order, fill_value=np.nan)

    df_f.rename(columns ={'libetab' : 'Etablissement'}, inplace = True)

    last_row_index = df_f.index[-1]
    new_table = html.Div(dash_table.DataTable(
        data=df_f.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_f.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'height': 'auto', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', 'whiteSpace': 'normal'},
        style_data_conditional=[{'if': {'row_index': last_row_index},'backgroundColor': '#FF4136','color': 'white' },
           ]
        ),
    )
    # Calculer la somme de la variable col_sum
    effectif_total = html.H5(f"Effectif total : {int(sum(col_sum))}")
    return new_table, effectif_total