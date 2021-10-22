'''
    olympics.py
    10/2/2021

    Simon Hempel-Costello
'''
import argparse
#Simply controls the user interfacing with the sql data
class Olympics_User_Interface():
    
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
        #parsing for NOC search
        NOC_name_parser.add_argument(
            'nocsearch',
            help = self.nocsearch_help,
            default  = '',
            nargs='?',
        )
        #parsing for medal list
        medal_parser = subparsers.add_parser('medallist',help =self.medallist_help)
        medal_parser.add_argument(
            'medallist',
            help = self.medallist_help,
            default  = '',
            action='store_true'
        )
        #parsing for agesearch search
        age_search = subparsers.add_parser('agesearch',help = self.agesearch_help)
        age_search.add_argument(
            'agesearch',
            help = self.agesearch_help,
            default  = '',
            nargs='?',
        )
        #start age parsing
        age_search.add_argument(
            '--startage','-s',
            help = self.startage_help,
            default = None, 

        )
        #end age parsing
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
#Allows for the queries to be made and prints out the results
class Olympics_SQL_Interface():
    def __init__(self):
        pass
    def establish_connection(self):
        # Connect to the database
        try:
            self.connection = psycopg2.connect(database=database, user=user, password=password)
        except Exception as e:
            print(e)
            exit()
        self.cursor = self.connection.cursor()

    def nocsearch_sql(self, input):
        #Searches for distinct olympians where there NOC ID matches the input one
        search_string = input.nocsearch
        query = '''SELECT DISTINCT olympians.firstname, olympians.surname, olympians.athlete_id
                    FROM olympians, competitor_instance
                    WHERE olympians.athlete_id = competitor_instance.olympian_id
                    AND competitor_instance.NOC_id =  %s
                    ORDER BY olympians.surname'''
        try:
            self.cursor.execute(query, (search_string,))
        except Exception as e:
            print(e)
            exit()
        #ensures that an actual NOC was input
        if(self.cursor.rowcount ==0):
            raise ValueError("please input a valid NOC acronym")
        print('=====Athletes From '+ search_string + '=====')
        for row in self.cursor:
            print(row[0] + row[1])

    def medallist_sql(self):
        #sql query for medal list
        query = '''SELECT competitor_instance.NOC_ID, COUNT(*) as "Number of Golds"
                FROM competitor_instance
                WHERE competitor_instance.medal = 'Gold'
                GROUP BY competitor_instance.NOC_id
                ORDER BY COUNT(*) DESC '''
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
            exit()
        print('====Nations By Gold Medal====')
        for row in self.cursor:
            print('Nation:'+row[0] +' Medals:' + str(row[1]))

    def agesearch_sql(self, input):
        start_age = 0
        end_age = 140
        if(input.startage != None):
            start_age = int(input.startage)
        if(input.endage != None):
            end_age = int(input.endage)
        #query for age search
        query = '''SELECT DISTINCT olympians.firstname, olympians.surname
                FROM olympians, competitor_instance
                WHERE olympians.athlete_id = competitor_instance.olympian_id
                AND competitor_instance.age BETWEEN %(start_age)s AND %(end_age)s
                ORDER BY olympians.surname
                '''
        #Dictionary for the possible variables in the query
        try:
            self.cursor.execute(query, ({'start_age':start_age, 'end_age':end_age}))
        except Exception as e:
            print(e)
            exit()
        for row in self.cursor:
            print(row[0] + row[1])
    def close_connection(self):
        self.connection.close()
if __name__ == '__main__':
    user_interface = Olympics_User_Interface()
    arguments = user_interface.get_arguements()
    sql_interface = Olympics_SQL_Interface()
    sql_interface.establish_connection()
    if('nocsearch' in arguments):
        sql_interface.nocsearch_sql(arguments)
    elif('medallist' in arguments):
        sql_interface.medallist_sql()
    elif('agesearch' in arguments):
        sql_interface.agesearch_sql(arguments)
    sql_interface.close_connection()
