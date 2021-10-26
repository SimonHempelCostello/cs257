#!/usr/bin/env python3
'''
    template_sample.py
    Jeff Ondich
    6 November 2020

    Using templates in Flask.
'''
import sys
import argparse
import flask
import json
from olympics import Olympics_SQL_Interface

app = flask.Flask(__name__)
sql_interface = Olympics_SQL_Interface()
sql_interface.establish_connection()
@app.route('/')
def home():
    return flask.render_template('help.html')

@app.route('/games')
def games():
    return sql_interface.json_output_games_list()

@app.route('/nocs')
def nocs():
    return sql_interface.json_output_noc_list()

@app.route('/medalists/games/<game>')
def shared_header_catchall(game):

    noc = flask.request.args.get('noc')
    return sql_interface.json_output_games_medal_list(game, noc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application demonstrating templates.')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
