'''
    olympics.py
    10/2/2021

    Simon Hempel-Costello
'''
import argparse
import json
class Olympics_User_Interface():
    '''Simply controls the user interfacing with the sql data''' 

    def __init__(self) -> None:
        self.nocsearch_help = 'Given a NOC search string, show the names of athletes who have represented that NOC ordered by their last name'
        self.medallist_help = 'Lists all NOCs in order of the gold medals they have won, in decreasing order of gold medals'
        self.agesearch_help = '''Given a youngest age, oldest age, or both, will search for olympians within the given ages inclusive. 
        If a youngest age only is given, all athletes older than that will be presented, vice versa for oldest.'''
        self.startage_help = 'youngest age to be included in output'
        self.endage_help = 'oldest age to be included in output'

    def get_arguements(self):
        parser = argparse.ArgumentParser('Allows for searches to be made around a database of olympic athletes')
        subparsers = parser.add_subparsers(description = 'commands')
        NOC_name_parser = subparsers.add_parser('nocsearch',help = self.nocsearch_help)
        '''parsing for NOC search'''
        NOC_name_parser.add_argument(
            'nocsearch',
            help = self.nocsearch_help,
            default  = '',
            nargs='?',
        )
        '''parsing for medal list'''
        medal_parser = subparsers.add_parser('medallist',help =self.medallist_help)
        medal_parser.add_argument(
            'medallist',
            help = self.medallist_help,
            default  = '',
            action='store_true'
        )
        '''parsing for agesearch search'''
        age_search = subparsers.add_parser('agesearch',help = self.agesearch_help)
        age_search.add_argument(
            'agesearch',
            help = self.agesearch_help,
            default  = '',
            nargs='?',
        )
        '''start age parsing'''
        age_search.add_argument(
            '--startage','-s',
            help = self.startage_help,
            default = None, 

        )
        '''end age parsing'''
        age_search.add_argument(
            '--endage','-e',
            help = self.endage_help,
            default = None
        )
        args = parser.parse_args()
        return args

import psycopg2
from config import password
from config import database
from config import user

class Olympics_SQL_Interface():
    '''Allows for the queries to be made and prints out the results'''

    def __init__(self):
        pass

    def establish_connection(self):
        ''' Connect to the database'''
        try:
            self.connection = psycopg2.connect(database=database, user=user, password=password)
        except Exception as e:
            print(e)
            exit()

    def nocsearch_sql(self, input):
        '''Searches for distinct olympians where there NOC ID matches the input one'''
        cursor = self.connection.cursor()
        search_string = input.nocsearch.upper()
        query = '''SELECT DISTINCT olympians.firstname, olympians.surname, olympians.athlete_id
                    FROM olympians, competitor_instance
                    WHERE olympians.athlete_id = competitor_instance.olympian_id
                    AND competitor_instance.NOC_id =  %s
                    ORDER BY olympians.surname'''
        try:
            cursor.execute(query, (search_string,))
        except Exception as e:
            print(e)
            exit()
        '''ensures that an actual NOC was input'''
        if(cursor.rowcount ==0):
            raise ValueError("please input a valid NOC acronym")
        return cursor

    def noc_printout(self, input):
        cursor = self.nocsearch_sql(input)
        search_string = input.nocsearch
        print('=====Athletes From National Olympic Committee '+ search_string + '=====')
        for row in cursor:
            print(row[0] + row[1])

    def medallist_sql(self):
        '''sql query for medal list'''
        cursor = self.connection.cursor()
        query = '''SELECT competitor_instance.NOC_ID, COUNT(*) as "Number of Golds"
                FROM competitor_instance
                WHERE competitor_instance.medal = 'Gold'
                GROUP BY competitor_instance.NOC_id
                ORDER BY COUNT(*) DESC '''
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()
        return cursor

    def medallist_printout(self):
        cursor = self.medallist_sql()
        print('====Nations By Gold Medal====')
        for row in cursor:
            print('Nation:'+row[0] +' Medals:' + str(row[1]))

    def agesearch_sql(self, input):
        '''sql for age search'''
        cursor = self.connection.cursor()
        start_age = 0
        end_age = 140
        if(input.startage != None):
            start_age = int(input.startage)
        if(input.endage != None):
            end_age = int(input.endage)
        '''query for age search'''
        query = '''SELECT DISTINCT olympians.firstname, olympians.surname
                FROM olympians, competitor_instance
                WHERE olympians.athlete_id = competitor_instance.olympian_id
                AND competitor_instance.age BETWEEN %(start_age)s AND %(end_age)s
                ORDER BY olympians.surname
                '''
        '''Dictionary for the possible variables in the query'''
        try:
            cursor.execute(query, ({'start_age':start_age, 'end_age':end_age}))
        except Exception as e:
            print(e)
            exit()
        return cursor

    def agesearch_printout(self, input):
        cursor = self.agesearch_sql(input)

        for row in cursor:

            print(row[0] + row[1])

    def noc_list(self):
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
        cursor = self.noc_list()
        output_list = []
        for row in cursor:
            row_dictionary = {}
            row_dictionary["noc_id"] = row[0]
            row_dictionary["region"] = row[1]
            output_list.append(row_dictionary)
        return json.dumps(output_list)


    def games_list(self):
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
        cursor = self.games_list()
        output_list = []
        for row in cursor:
            row_dictionary = {}
            row_dictionary["id"] = row[0]
            row_dictionary["year"] = row[1]
            row_dictionary["season"] = row[2]
            row_dictionary["city"] = row[3]


            output_list.append(row_dictionary)
        return json.dumps(output_list)

    def games_medal_list(self,games_input, NOC_input = None):
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

    def json_output_games_medal_list(self, games_input, NOC_input = None):
        '''returns the JSON output contaning the data from the games medal list sql call'''
        cursor = self.games_medal_list(games_input,NOC_input)
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

if __name__ == '__main__':
    sql_interface = Olympics_SQL_Interface()
    sql_interface.establish_connection()
    user_interface = Olympics_User_Interface()
    arguments = user_interface.get_arguements()
    if('nocsearch' in arguments):
        sql_interface.noc_printout(arguments)
    elif('medallist' in arguments):
        sql_interface.medallist_printout()
    elif('agesearch' in arguments):
        sql_interface.agesearch_printout(arguments)
    sql_interface.close_connection()
