import pandas as pd
import dash
import dash_html_components as html
from dash import dash_table, Output, Input, State, callback
from read_data import df
import dash_core_components as dcc
from function import move_rows
import dash_bootstrap_components as dbc
import numpy as np

# Initialiser l'application Dash
df1 = df.loc[df['libetab'] == 'CLG ALBERT CAMUS']
df1 = pd.pivot_table(df1, values='num', index=['libetab', 'nom_ut'], columns='libpcs', aggfunc=len)
df1 = df1.reset_index()
del df1[df1.columns[0]]

# # Liste des colonnes à réordonner
col_order = ['nom_ut', 'Cadres supérieurs et enseignants', 'Cadres moyens', 'Employés, artisans, commerçants et agriculteurs', 'Ouvriers et inactifs', 'Non renseignée']
df1 = df1.reindex(columns=col_order, fill_value=0)
# df1.rename(columns ={'nom_ut' : 'Unité territoriale'}, inplace = True)




# Création du layout
# app.layout
simulations_layout = html.Div(
    dbc.Container(
            [html.Div(className="sticky-dropdowns", style={'position': 'sticky', 'top': '0', 'zIndex': 1}, children=[
        html.Div([
            html.H6('Collège 1'),
            dcc.Dropdown(
                id='table1-dropdown',
                options=[{'label': str(val), 'value': str(val)} for val in df.libetab.unique()],
                value=str(df.libetab.unique()[0]),
                clearable=False,
                placeholder="Sélectionnez une option",
                # style={'fontSize': '10px'}
            ),
            html.Div(dash_table.DataTable(
                id='table1',
                # data=selected_rows.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df1.columns],
                data=[],
                row_selectable="single",
                selected_rows=[],
                style_table={'overflowX': 'auto', 'width': '100%'},
                style_cell={'height': 'auto', 'minWidth': '40px', 'width': '80px', 'maxWidth': '160px','lineHeight':'15px', 'whiteSpace': 'normal'
                        }), style={'marginTop': 20, 'maxHeight': '500px', 'overflow-y': 'scroll'} )

        ], style={'display': 'inline-block', 'width': '48%', 'marginRight': '2%'}),
        html.Div([
            html.H6('Collège 2'),
            dcc.Dropdown(
                id='table2-dropdown',
                options=[{'label': str(val), 'value': str(val)} for val in df.libetab.unique()],
                value=str(df.libetab.unique()[0]),
                clearable=False,
                placeholder="Sélectionnez une option"
            ),
            # Tableau pour afficher les données
            html.Div(id='table2', className='table-responsive', style={'marginTop': 20, 'maxHeight': '500px', 'overflow-y': 'scroll'}),
        ], style={'display': 'inline-block', 'width': '48%', 'marginLeft': '2%'}),
        ###########################################################################
        ##############################  partie simulation  #######################
        html.Div(
            className="d-flex align-items-center justify-content-center", style={"height": "100%"},
            children=[html.Button("Faire une simulation", id="button", n_clicks=0, className="btn btn-primary mx-auto",),],
        ),
        html.H6(id='selected_ut'),
            html.Div(id='div_style', children=[
                dbc.Row([
                    dbc.Col(html.Div([
                        html.Div([
                            html.H5('IPS avant simulation'),
                            html.Div(id='ips01'),
                            html.Div(id='std_ips01'),

                            html.H5('IPS apès simulation'),
                            html.Div(id='ips1'),
                            html.Div(id='std_ips1')
                        ]),
                        html.Div(id='table1_sim', className='table-responsive', style={'marginTop': 20, 'maxHeight': '500px', 'overflow-y': 'scroll'}),
                    ], style={'margin-top': '5%'}), width=6),
                    dbc.Col(html.Div([
                        html.Div([
                            html.H5('IPS avant simulation'),
                            html.Div(id='ips02'),
                            html.Div(id='std_ips02'),

                            html.H5('IPS apès simulation'),     
                            html.Div(id='ips2'),
                            html.Div(id='std_ips2')
                        ]),
                        html.Div(id='table2_sim', className='table-responsive', style={'marginTop': 20, 'maxHeight': '500px', 'overflow-y': 'scroll'}),
                    ], style={'margin-top': '5%', 'margin-left': '2%'}), width=6),
                ]),
            ]),
        ]),
    ]), style={'fontSize': '12px'}
)


# Callback pour mettre à jour le tableau 1
@callback(
    Output('table1', 'data'),
    # Output('table1', 'children'),
    [Input('table1-dropdown', 'value')]
)
def update_table1(selected_table):
    if not selected_table:
        # Si aucune option n'a été sélectionnée, renvoyer une liste vide
        return []
    else:
        # Sinon, filtrer les données en fonction de la valeur sélectionnée et renvoyer les données filtrées sous forme de liste
        df_filtered = df.loc[df['libetab'] == selected_table]
        table = pd.pivot_table(df_filtered, values='num', index=['nom_ut'], columns='libpcs', aggfunc=len)
        selected_rows = table.reset_index()
        selected_rows = selected_rows.sort_values(by=['nom_ut'])
        return selected_rows.to_dict('records')

# Callback pour mettre à jour le tableau 2
@callback(
    Output('table2', 'children'),
    [Input('table2-dropdown', 'value')]
)
def update_table2(selected_table):
    df_filtered = df.loc[df['libetab'] == selected_table]
    table = pd.pivot_table(df_filtered, values='num', index=['nom_ut'], columns='libpcs', aggfunc=len)
    selected_rows = table.reset_index()
    selected_rows = selected_rows.sort_values(by=['nom_ut'])

        # # Liste des colonnes à réordonner
    col_order = ['nom_ut', 'Cadres supérieurs et enseignants', 'Cadres moyens', 'Employés, artisans, commerçants et agriculteurs', 'Ouvriers et inactifs', 'Non renseignée']
    selected_rows = selected_rows.reindex(columns=col_order, fill_value=0)

    new_table = html.Div(dash_table.DataTable(
        data=selected_rows.to_dict('records'),
        columns=[{"name": i, "id": i} for i in selected_rows.columns],
        # row_selectable="single",
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_cell={'height': 'auto', 'minWidth': '40px', 'width': '80px', 'maxWidth': '160px','lineHeight':'15px', 'whiteSpace': 'normal'
                        }))
    return new_table

@callback(
    [Output('selected_ut', 'children'),
     Output('table1_sim', 'children'),
     Output('table2_sim', 'children'),

     Output('ips01', 'children'),
     Output('std_ips01', 'children'),
     Output('ips02', 'children'),
     Output('std_ips02', 'children'),

     Output('ips1', 'children'),
     Output('std_ips1', 'children'),
     Output('ips2', 'children'),
     Output('std_ips2', 'children'),
     Output('div_style', 'style')],
    [Input('table1', 'selected_rows'),
     Input('button', 'n_clicks')],
    [State('table1', 'data'),
     State('table1-dropdown', 'value'),
     State('table2-dropdown', 'value')])

def get_selected_row_indices(selected_columns,n_clicks, table_data, dropdown1, dropdown2):
    if n_clicks:
        if dropdown1 == dropdown2 :
            div_style = {'display': 'none'}
            return (html.Span("Vous ne pouvez pas choisir le même collège", style={'color': 'red'}), [], [], '', '', '', '', '', '', '', '', div_style)
        elif dropdown1 != dropdown2 :
            if selected_columns:
                df_filtered1 = df.loc[df['libetab'] == dropdown1]
                df_filtered2 = df.loc[df['libetab'] == dropdown2]

                ips01 = round(np.mean(df_filtered1.code_ips),2)
                std_ips01 = round(np.std(df_filtered1.code_ips),2)
                ips02 = round(np.mean(df_filtered2.code_ips),2)
                std_ips02 = round(np.std(df_filtered2.code_ips),2)

                selected_data = [table_data[i] for i in selected_columns]
                nom_ut = selected_data[0]['nom_ut'] # récupérer la valeur de la colonne 'nom_ut' de la première ligne sélectionnée
                df1_simulation, df2_simulation = move_rows(df_filtered1, df_filtered2, 'nom_ut',  nom_ut)

                ips1 = round(np.mean(df1_simulation.code_ips),2)
                std_ips1 = round(np.std(df1_simulation.code_ips),2)
                ips2 = round(np.mean(df2_simulation.code_ips),2)
                std_ips2 = round(np.std(df2_simulation.code_ips),2)

                table = pd.pivot_table(df1_simulation, values='num', index=['nom_ut'], columns='libpcs', aggfunc=len)
                df1_simulation = table.reset_index()
                df1_simulation = df1_simulation.sort_values(by=['nom_ut'])

                        # # Liste des colonnes à réordonner
                col_order = ['nom_ut', 'Cadres supérieurs et enseignants', 'Cadres moyens', 'Employés, artisans, commerçants et agriculteurs', 'Ouvriers et inactifs', 'Non renseignée']
                df1_simulation = df1_simulation.reindex(columns=col_order, fill_value=0)

                table = pd.pivot_table(df2_simulation, values='num', index=['nom_ut'], columns='libpcs', aggfunc=len)
                df2_simulation = table.reset_index()
                df2_simulation = df2_simulation.sort_values(by=['nom_ut'])

                # # Liste des colonnes à réordonner
                col_order = ['nom_ut', 'Cadres supérieurs et enseignants', 'Cadres moyens', 'Employés, artisans, commerçants et agriculteurs', 'Ouvriers et inactifs', 'Non renseignée']
                df2_simulation = df2_simulation.reindex(columns=col_order, fill_value=0)

                div_style = {'display': 'block'}

                return (
                    f"L'ut : {nom_ut} est déplacée de {dropdown1} vers {dropdown2}",
                    html.Div(dash_table.DataTable(
                        data=df1_simulation.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df1_simulation.columns],
                        # sort_action='native',
                        style_table={'overflowX': 'auto'},
                         style_cell={
                            'height': 'auto', 'minWidth': '40px', 'width': '80px', 'maxWidth': '160px','lineHeight':'15px', 'whiteSpace': 'normal'
                        })),
                    html.Div(dash_table.DataTable(
                        data=df2_simulation.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df2_simulation.columns],
                        # sort_action='native',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto', 'minWidth': '40px', 'width': '80px', 'maxWidth': '160px','lineHeight':'15px', 'whiteSpace': 'normal'
                        })),
                    f"IPS : {ips01}",
                    f"Ecart type : {std_ips01}",
                    f"IPS : {ips02}",
                    f"Ecart type : {std_ips02}",

                    f"IPS : {ips1}",
                    f"Ecart type : {std_ips1}",
                    f"IPS  : {ips2}",
                    f"Ecart type : {std_ips2}",
                    div_style
                )
            else :
                div_style = {'display': 'none'}
                return (html.Span("Aucune UT n'est sélectionnée", style={'color': 'red'}) , [], [], '', '', '', '','', '', '', '', div_style)

    else:
        div_style = {'display': 'none'}
        # return (html.Span("Aucune UT n'est sélectionnée", style={'color': 'red'}) , [], [], '', '', '', '','', '', '', '', div_style) # retourner une liste vide et des chaînes vides pour les sorties correspondant aux Data Tables et aux valeurs de IPS et STD IPS
        return ('' , [], [], '', '', '', '','', '', '', '', div_style) # retourner une liste vide et des chaînes vides pour les sorties correspondant aux Data Tables et aux valeurs de IPS et STD IPS



# # Lancement de l'application Dash
# if __name__ == '__main__':
#     app.run_server(debug=True)
