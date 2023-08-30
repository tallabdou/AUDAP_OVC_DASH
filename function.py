import pandas as pd

def move_rows(df1, df2, var_ut, ut_depl):
    # Trouver toutes les lignes de df1 où la colonne 'x' est égale à 'oui'
    mask = df1[var_ut] == ut_depl
    # Copier les lignes correspondantes de df1 dans df2
    df2 = pd.concat([df2, df1.loc[mask]])
    # Supprimer les lignes correspondantes de df1
    df1 = df1.loc[~mask]
    return df1, df2
