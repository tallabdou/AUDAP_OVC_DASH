import dash
import dash_core_components as dcc
from dash import dash_table
import dash_html_components as html
from read_data import df
from dash.dependencies import Input, Output
from dash import callback
import pandas as pd


college_layout = html.Div([
    html.H1("Collège"),
    dcc.Dropdown(
        id='index-value-dropdown-colleges',
        options=[{'label': str(val), 'value': str(val)} for val in df.libetab.unique()],
        value=str(df.libetab.unique()[0]),
        clearable=False,
        style={'width': '50%'} 
    ),
    html.Div(id='table-body-colleges', className='table-responsive', style={'marginTop': 20}),
    html.Div(id='effectif-total-colleges', style={'marginTop': 20})
    ], className='container')


@callback(
    [Output('table-body-colleges', 'children'),
     Output('effectif-total-colleges', 'children')],
    Input('index-value-dropdown-colleges', 'value'),
    )
def update_table(index_value):
    df_filtered = df.loc[df['libetab'] == index_value]
    table = pd.pivot_table(df_filtered, values='num', index=['nom_ut'], columns='libpcs', aggfunc=len)

    col_sum = table.sum(axis=0, skipna=True)
    selected_rows = round((table / col_sum) * 100,2)

    selected_rows = selected_rows.reset_index()
    selected_rows = selected_rows.sort_values(by=['nom_ut'])
    
    # Ajouter la somme des colonnes à la dernière ligne avec 'Total' dans la première colonne
    col_sum_pour = round((col_sum / sum(col_sum)) * 100,2)
    new_row_pour = pd.DataFrame({selected_rows.columns[0]: 'Pourcentage CSP', 
                            selected_rows.columns[1]: col_sum_pour.iloc[0], selected_rows.columns[2]: col_sum_pour.iloc[1],
                            selected_rows.columns[3]: col_sum_pour.iloc[2],selected_rows.columns[4]: col_sum_pour.iloc[3]
                            ,selected_rows.columns[5]: col_sum_pour.iloc[4]}, index=[3])
    
    # Ajouter la somme des colonnes à la dernière ligne avec 'Total' dans la première colonne
    new_row = pd.DataFrame({selected_rows.columns[0]: 'Total colonne', 
                            selected_rows.columns[1]: col_sum.iloc[0], selected_rows.columns[2]: col_sum.iloc[1],
                            selected_rows.columns[3]: col_sum.iloc[2],selected_rows.columns[4]: col_sum.iloc[3]
                            ,selected_rows.columns[5]: col_sum.iloc[4]}, index=[3])
    
    df_f = pd.concat([selected_rows, new_row_pour, new_row], ignore_index=True)

    # Liste des colonnes à réordonner
    col_order = ['nom_ut', 'Cadres supérieurs et enseignants', 'Cadres moyens', 'Employés, artisans, commerçants et agriculteurs', 'Ouvriers et inactifs', 'Non renseignée']
    df_f = df_f.reindex(columns=col_order, fill_value=0)
    df_f.rename(columns ={'nom_ut' : 'Unité territoriale'}, inplace = True)

    last_row_index = df_f.index[-1]
    before_last_row_index = df_f.index[-2]
    # Créer une nouvelle table HTML pour afficher les données
    new_table = html.Div(dash_table.DataTable(
        data=df_f.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_f.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'height': 'auto', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', 'whiteSpace': 'normal'},
        style_data_conditional=[{'if': {'row_index': last_row_index},'backgroundColor': '#FF4136','color': 'white' },
            {'if': {'row_index': before_last_row_index},'backgroundColor': 'RebeccaPurple','color': 'white' },]
        ),
    )
    # Calculer la somme de la variable col_sum
    effectif_total = html.H5(f"Effectif total : {int(sum(col_sum))}")
    return new_table, effectif_total