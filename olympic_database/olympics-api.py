#!/usr/bin/env python3
'''
    olympics-api.py
    10/25/2021

    Simon Hempel-Costello
'''
import sys
import argparse
import flask
import json
import psycopg2
from config import password
from config import database
from config import user

class JSON_SQL_Olympics_Interface():
    '''Allows for the queries to be made and prints out the results, also I initially had this as part of the olympics.py sql interface, and if 
    this were the actual project I would likely keep it there, but I moved it here for clarity with the actual assignment'''

    def __init__(self):
        pass

    def establish_connection(self):
        ''' Connect to the database'''
        try:
            self.connection = psycopg2.connect(database=database, user=user, password=password)
        except Exception as e:
            print(e)
            exit()

    def noc_list_sql(self):
        '''sql query for noc list'''
        cursor = self.connection.cursor()
        query = '''SELECT  noc_regions.NOC_id, noc_regions.region
                FROM noc_regions
                ORDER BY noc_regions.NOC_id'''
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()
        return cursor

    def json_output_noc_list(self):
        '''returns json output for the noc list sql call'''
        cursor = self.noc_list_sql()
        output_list = []
        for row in cursor:
            row_dictionary = {}
            row_dictionary["noc_id"] = row[0]
            row_dictionary["region"] = row[1]
            output_list.append(row_dictionary)
        return json.dumps(output_list)


    def games_list_sql(self):
        '''sql query for games list'''
        cursor = self.connection.cursor()
        query = '''SELECT  games.id, games.year, games.season, games.city
                FROM games
                ORDER BY games.year'''
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()
        return cursor

    def json_output_games_list(self):
        '''returns the json output containing the data from the games list sql call'''
        cursor = self.games_list_sql()
        output_list = []
        for row in cursor:
            row_dictionary = {}
            row_dictionary["id"] = row[0]
            row_dictionary["year"] = row[1]
            row_dictionary["season"] = row[2]
            row_dictionary["city"] = row[3]
            output_list.append(row_dictionary)
        return json.dumps(output_list)

    def games_medalists_sql(self,games_input, NOC_input = None):
        '''sql for getting the list of medals at a specified games from a certain dictionary'''
        cursor = self.connection.cursor()

        if(NOC_input == None):
            query = '''SELECT DISTINCT olympians.athlete_id, olympians.firstname, olympians.surname, competitor_instance.sex, competitor_instance.medal, events.sport, events.olympic_event
                    FROM games, olympians, competitor_instance, events
                    WHERE events.game_id = %(games_id)s
                    AND competitor_instance.event_id = events.id
                    AND olympians.athlete_id = competitor_instance.olympian_id
                    AND competitor_instance.medal != 'NULL' '''
            try:
                cursor.execute(query, ({'games_id':games_input}))
            except Exception as e:
                print(e)
                exit()
        else:
            query = '''SELECT DISTINCT olympians.athlete_id, olympians.firstname, olympians.surname, competitor_instance.sex, competitor_instance.medal, events.sport, events.olympic_event
                    FROM games, olympians, competitor_instance, events
                    WHERE events.game_id = %(games_id)s
                    AND competitor_instance.event_id = events.id
                    AND olympians.athlete_id = competitor_instance.olympian_id
                    AND competitor_instance.medal != 'NULL'
                    AND %(noc_id)s = competitor_instance.NOC_id'''
            try:
                cursor.execute(query, ({'games_id':games_input, 'noc_id':NOC_input}))
            except Exception as e:
                print(e)
                exit()
        return cursor

    def json_output_games_medalists(self, games_input, NOC_input = None):
        '''returns the JSON output contaning the data from the games medal list sql call'''
        cursor = self.games_medalists_sql(games_input,NOC_input)
        output_list = []
        for row in cursor:
            row_dictionary = {}
            row_dictionary["athlete_id"] = row[0]
            row_dictionary["name"] = row[1] + " " + row[2]
            row_dictionary["sex"] = row[3]
            row_dictionary["medal"] = row[4]
            row_dictionary["sport"] = row[5]
            row_dictionary["event"] = row[6]
            output_list.append(row_dictionary)
        return json.dumps(output_list)

    def close_connection(self):
        self.connection.close()

app = flask.Flask(__name__)
sql_interface = JSON_SQL_Olympics_Interface()
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
    return sql_interface.json_output_games_medalists(game, noc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application demonstrating templates.')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
