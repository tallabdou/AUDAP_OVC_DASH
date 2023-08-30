import pandas as pd
import psycopg2

import numpy as np
import geopandas as gpd
from shapely import wkb
import folium
from shapely.geometry import Point

conn = psycopg2.connect(
    host="10.96.49.6",
    database="dev.audap.org",
    user="a.tall",
    password="Duj86362")

## importer les collèges
sql_select = '''SELECT *
    FROM ovc.adresses_ut
    where secteur = 'PU' and etab in 
    ('0640606L', '0641413N', '0640607M', '0640227Z', '0642095E', '0641411L', '0641391P', '0640608N');'''
palois = pd.read_sql_query(sql_select, conn)

###########################  Analyse des colléges  ######################################
####  calcul de l'IPS et du std
mean_by_group = palois.groupby(['etab','libcommune','libetab'])['ips_eleve'].mean()
std_by_group = palois.groupby(['etab','libcommune','libetab'])['ips_eleve'].std()
nbr_collegiens = palois.groupby(['etab','libcommune','libetab'])['ips_eleve'].size()
nom_data = palois.groupby(['etab','libcommune','libetab'])['nom'].apply(lambda x: ', '.join(map(str, set(x))))

df_colleges = mean_by_group.reset_index()[['etab','libcommune','libetab']]

df_colleges = df_colleges.merge(mean_by_group.rename('ips_college'), on='etab')
df_colleges = df_colleges.merge(std_by_group.rename('ecart_type_ips_college'), on='etab')
df_colleges = df_colleges.merge(nbr_collegiens.rename('nbr_collegiens'), on='etab')
df_colleges = df_colleges.merge(nom_data.rename('ut'), on='etab')

####  Géolocalisation des colléges
sql_select = '''select t2.*
    from (SELECT distinct etab
    FROM ovc.cd64_adresses_collegiens
    where secteur = 'PU' and etab in ('0640606L', '0641413N', '0640607M', '0640227Z', '0642095E', '0641411L', '0641391P', '0640608N')) as t1
    inner join (SELECT id, nom, geom, libgeo
    FROM ovc.college) as t2
    on t1.etab = t2.id;'''
colleges_points = pd.read_sql_query(sql_select, conn)
## convertir en geom
def convert_to_geometry(geom_value):
    if not geom_value:
        ## Collège Pierre Emmanuel est géolocaliser manuellement
        return Point(-0.364252, 43.3048542)
    try:
        return wkb.loads(bytes.fromhex(geom_value))
    except:
        return None

colleges_points['geometry'] = colleges_points['geom'].apply(convert_to_geometry)

gdf_colleges = gpd.GeoDataFrame(colleges_points.dropna(subset=['geometry']), geometry='geometry')
gdf_colleges.drop(columns=['geom'], inplace=True)
### merger avec les données ips
gdf_colleges = pd.merge(gdf_colleges, df_colleges, left_on="id", right_on="etab")


###########################  Analyse des UT  ######################################
mean_ips_ut = palois.groupby(['id','nom'])['ips_eleve'].mean()
std_ips_ut = palois.groupby(['id','nom'])['ips_eleve'].std()
nbr_collegiens_ut = palois.groupby(['id','nom'])['ips_eleve'].size()
nom_data = palois.groupby(['id','nom'])['libetab'].apply(lambda x: ', '.join(map(str, set(x))))

df_ut = mean_ips_ut.reset_index()[['id','nom']]

df_ut = df_ut.merge(mean_ips_ut.rename('ips_ut'), on='nom')
df_ut = df_ut.merge(std_ips_ut.rename('ecart_type_ips_ut'), on='nom')
df_ut = df_ut.merge(nbr_collegiens_ut.rename('ips_nbr_collegiens'), on='nom')
df_ut = df_ut.merge(nom_data.rename('colleges'), on='nom')

## Contoure des UT : les hors dep ne sont pas pris en compte
sql_select = '''SELECT t1.*, codgeo, geom, libgeo, t3.*
FROM (
    SELECT DISTINCT id, nom_ut
    FROM ovc.cd64_adresses_collegiens
    WHERE secteur = 'PU' 
    AND (etab = '0642095E' OR id::integer IN (
        SELECT t11.unite_territoriale_id::integer
        FROM ovc.secteur t11
        LEFT JOIN ovc.unite_territoriale t22 ON t11.unite_territoriale_id = t22.id
        LEFT JOIN ovc.college t33 ON t11.college_id = t33.id
        WHERE t11.college_id IN ('0640606L', '0641413N', '0640607M', '0640227Z', '0642095E', '0641411L', '0641391P', '0640608N')
        AND t11.id != 470))
    ) AS t1
    INNER JOIN (
        SELECT id, nom, codgeo, geom, libgeo
        FROM ovc.unite_territoriale
    ) AS t2
    ON t1.id::integer = t2.id
    left join (SELECT  t12.unite_territoriale_id,
        t32.nom as college_nom
    FROM ovc.secteur t12
    LEFT JOIN ovc.unite_territoriale t22 ON t12.unite_territoriale_id = t22.id
    LEFT JOIN ovc.college t32 ON t12.college_id = t32.id
    WHERE t12.college_id IN ('0640606L', '0641413N', '0640607M', '0640227Z', '0642095E', '0641411L', '0641391P', '0640608N')
    and t12.id != 470) t3
    ON t1.id::integer = t3.unite_territoriale_id;'''
ut_geom = pd.read_sql_query(sql_select, conn)

##remplacer vide par collège Pierre Emmanuel
ut_geom['college_nom'].loc[ut_geom['college_nom'].isnull()] = 'Collège Pierre Emmanuel'

ut_geom['geometry'] = ut_geom['geom'].apply(lambda x: wkb.loads(bytes.fromhex(x)))
gdf_ut = gpd.GeoDataFrame(ut_geom, geometry='geometry')
gdf_ut.drop(columns=['geom'], inplace=True)
#### merger geom et ips
df_ut = df_ut.astype({'id':'int'}).astype({'id':'str'})
gdf_ut = gdf_ut.merge(df_ut, on='id')

######################  suite calcule df_ut  #######################
df_ut['id'] = df_ut['id'].astype('int')
df_ut = df_ut[df_ut['id'].isin(list(ut_geom['id'].astype('int').unique()))]
ut_geom = ut_geom.astype({'id':'int'})
df_ut0 = df_ut.merge(ut_geom[['id','college_nom']], on='id')
del df_ut0['colleges']
# print(df_ut0)
########################### Sectorisation : Analyse des collèges et UT  ######################################
sql_select = '''SELECT t1.college_id, t1.unite_territoriale_id, t2.nom as ut_nom, t2.geom as ut_geom,
       t3.nom as college_nom, t3.geom as college_geom, t3.libgeo, t3.sectorisation
FROM ovc.secteur t1
LEFT JOIN ovc.unite_territoriale t2 ON t1.unite_territoriale_id = t2.id
LEFT JOIN ovc.college t3 ON t1.college_id = t3.id
WHERE t1.college_id IN ('0640606L', '0641413N', '0640607M', '0640227Z', '0642095E', '0641411L', '0641391P', '0640608N')
and t1.id != 470;'''
### 470 pour exclure Gelos qui est dupliqué
palois_ut_co = pd.read_sql_query(sql_select, conn)

#####################                 ############################
palois_ut_co['geometry'] = palois_ut_co['ut_geom'].apply(lambda x: wkb.loads(bytes.fromhex(x)))
gpalois_ut_co = gpd.GeoDataFrame(palois_ut_co, geometry='geometry')
gpalois_ut_co.drop(columns=['ut_geom'], inplace=True)

#####################     jointure avec les collèges            ############################
gdf_ut_college = pd.DataFrame()
df_ut['id'] = df_ut['id'].astype('int')
gdf_ut_college = pd.merge(gpalois_ut_co, df_ut,  how='left', left_on=['unite_territoriale_id'], right_on = ['id'])
gdf_ut_college = pd.merge(gdf_ut_college, gdf_colleges,  how='left', left_on=['college_id'], right_on = ['id'])
gdf_ut_college['ips_ut'] = round(gdf_ut_college['ips_ut'],2)
gdf_ut_college = gdf_ut_college[['ut_nom','college_nom','geometry_x', 'geometry_y', 'libetab',
                                 'ips_ut','ecart_type_ips_ut', 'ips_nbr_collegiens']]