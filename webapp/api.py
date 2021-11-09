'''
    api.py
    Simon Hempel-Costello, 25 April 2016
    Updated 8 November 2021

    Tiny Flask API to support the tiny books web application.
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.username
                            )

@api.route('/authors/') 
def get_authors():
    ''' Returns a list of all the authors in our database. See
        get_author_by_id below for description of the author
        resource representation.

        By default, the list is presented in alphabetical order
        by surname, then given_name. You may, however, use
        the GET parameter sort to request sorting by birth year.

            http://.../authors/?sort=birth_year

        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT id, given_name, surname, birth_year, death_year
               FROM authors ORDER BY '''

    sort_argument = flask.request.args.get('sort')
    if sort_argument == 'birth_year':
        query += 'birth_year'
    else:
        query += 'surname, given_name'

    author_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            author = {'id':row[0],
                      'given_name':row[1],
                      'surname':row[2],
                      'birth_year':row[3],
                      'death_year':row[4]}
            author_list.append(author)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(author_list)

@api.route('/search/input/<search_query>')
def get_books_for_author(search_query):
    return json_output_tweet_search(search_query)

def tweet_search_sql(input_query):
    '''sql for getting the list of medals at a specified games from a certain dictionary'''
    cursor = get_connection().cursor()

    query = '''SELECT DISTINCT tweets.tweet_content, authors.author_name, tweet_instance.followers, tweet_instance.accounts_followed, tweets.publish_date
    FROM tweets, authors, tweet_instance
    WHERE authors.external_author_id = tweet_instance.author_id
    AND tweets.tweet_id = tweet_instance.tweet_id
    and tweets.tweet_content LIKE %(input_query)s'''
        
    try:
        cursor.execute(query, ({'input_query':'%'+input_query+'%'}))
    except Exception as e:
        print(e)
        exit()
    return cursor
def json_output_tweet_search( query):
    '''returns the JSON output contaning the data from the games medal list sql call'''
    cursor = tweet_search_sql(query)
    output_list = []
    for row in cursor:
        row_dictionary = {}
        row_dictionary["content"] = row[0]
        row_dictionary["author_name"] = row[1]
        row_dictionary["followers"] = row[2]
        row_dictionary["followed"] = row[3]
        row_dictionary["date"] = row[4]
        output_list.append(row_dictionary)
    print(output_list)
    return json.dumps(output_list)