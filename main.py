import dash
import dash_bootstrap_components as dbc
from flask import Flask
from navbar import app_dash_file

app = Flask(__name__)
dash_app = dash.Dash(__name__, server = app, suppress_callback_exceptions=True,  url_base_pathname='/ovc64/',
external_stylesheets =[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.9.0/css/all.css'])


app_dash_file(dash_app)

if __name__ == "__main__":
    app.run(host='10.96.49.7', port=8506)

