import json
import config
import psycopg2
def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.username
                            )


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
    return json.dumps(output_list)