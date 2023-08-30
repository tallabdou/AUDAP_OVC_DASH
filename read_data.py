import pandas as pd
import psycopg2


conn = psycopg2.connect(
    host="10.96.49.6",
    database="dev.audap.org",
    user="a.tall",
    password="Duj86362")

sql_select = '''SELECT etab, libcommune, libetab, secteur, ips_etab, libstat4, lien1, lib_lien1, nivresp1, lib_nivresp1, pcs1, pcs1r, lib_pcs1r as libpcs, lien2, lib_lien2, nivresp2, lib_nivresp2, pcs2, pcs2r, lib_pcs2r, adr1_comres, adr2_comres, cp_comres, insee_commres, lib_comres, latitude, longitude, num, ips_eleve as code_ips, geom, id, nom as nom_ut, codgeo, libgeo
	FROM ovc.adresses_ut;'''
df = pd.read_sql_query(sql_select, conn)
