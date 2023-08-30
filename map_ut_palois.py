import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

def f_map_ut_colleges_palois(xx, var, popup1, popup2, popup3, popup4, popup5) :


    ## carte en arrière plan
    mymap = folium.Map(location=[xx['geometry'].centroid.y.mean(), xx['geometry'].centroid.x.mean()], zoom_start=8,tiles=None)
    folium.TileLayer('cartodbpositron',name="Light Map",control=False).add_to(mymap)
    xx.crs = "EPSG:4326"

    bins2 = (xx[var].quantile((0,0.25,0.5,0.75,1))).tolist()

    mymap.choropleth(
     geo_data=xx,
     name='Choropleth',
     data=xx,
    ## variable dans colonnes doit etrer la meme que 'key_on'
     columns=['id',var],
     key_on="feature.properties.id",
     fill_color='YlGnBu',
    #  threshold_scale=myscale,
     
     bins=bins2,
     fill_opacity=1,
     line_opacity=0.2,
     legend_name='Médiane du prix moyen du mètre carré',
     smooth_factor=0
    )
    ##paramètre d'affichage
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    NIL = folium.features.GeoJson(
        xx,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
             fields=[popup1, popup2, popup3, popup4, popup5],
            aliases=['UT: ', 'IPS: ','Ecart-type: ', 'Nbr de collégiens: ', 'Collège: ' ],

        )
    )
    
    mymap.add_child(NIL)
    mymap.keep_in_front(NIL)
    folium.LayerControl().add_to(mymap)
    ############  #######################

    return mymap