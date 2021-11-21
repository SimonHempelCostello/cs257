'''
    sql_interface.py
    Simon Hempel-Costello, Lev Schuster
    11 November 2021
'''
import json
import config
import psycopg2

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database, user=config.user)

def tweet_search_sql(input_query, sorting_metric, start_date, end_date):
    '''sql for getting the list of matching bots'''
    cursor = get_connection().cursor()
    sort_by =''
    order = ''
    if(sorting_metric == 'Followers'):
        sort_by = 'tweet_instance.followers'
        order = ' DESC'
    elif(sorting_metric == 'Following'):
        sort_by = 'tweet_instance.accounts_followed'
        order = ' DESC'
    elif(sorting_metric == 'Alphabetically'):
        sort_by = 'authors.author_name'
        order = ' ASC'
    

    query = '''SELECT DISTINCT tweets.tweet_content, authors.author_name, 
    tweet_instance.followers, tweet_instance.accounts_followed, tweets.publish_date
    FROM tweets, authors, tweet_instance
    WHERE authors.external_author_id = tweet_instance.author_id
    AND tweets.tweet_id = tweet_instance.tweet_id
    AND tweets.publish_date >= %(start_date)s AND tweets.publish_date < %(end_date)s
    AND tweets.tweet_content LIKE %(input_query)s
    ORDER BY ''' + sort_by + order
        
    try:
        cursor.execute(query, ({'input_query':'%'+input_query+'%', 'start_date':start_date, 'end_date':end_date}))
    except Exception as e:
        print(e)
        exit()
    return cursor

def json_output_tweet_search(search_query = '', sorting_metric = 'Followers', start_date = '2012/01/01', end_date = '2018/05/31'):
    '''returns the JSON output contaning the data from the matching tweets'''
    cursor = tweet_search_sql(search_query, sorting_metric, start_date, end_date)
    output_list = []
    for row in cursor:
        row_dictionary = {}
        row_dictionary["content"] = row[0]
        row_dictionary["author_name"] = row[1]
        row_dictionary["followers"] = row[2]
        row_dictionary["followed"] = row[3]
        row_dictionary["date"] = row[4]
        output_list.append(row_dictionary)
    print(json.dumps(output_list))
    return json.dumps(output_list)

def user_rankings_sql(sort_metric, start_date, end_date, hide_original_tweets, hide_retweets):
    '''sql for getting the list of highest performing bots'''
    cursor = get_connection().cursor()
    hide_value = 2
    sort_by = ''
    if(hide_original_tweets and hide_retweets):
        return None
    elif(hide_original_tweets):
        hide_value = 0
    elif(hide_retweets):
        hide_value = 1
        
    if(sort_metric == 'Following'):
        sort_by = 'MAX(tweet_instance.accounts_followed)'
    elif(sort_metric == 'Followers'):
        sort_by = 'MAX(tweet_instance.followers)'
    elif(sort_metric =='Tweet Count' ):
        sort_by = 'COUNT(tweet_instance)'
        
    query = '''SELECT DISTINCT authors.author_name,''' + sort_by + ''' 
    FROM authors, tweet_instance, tweets
    WHERE tweet_instance.author_id = authors.external_author_id
    AND tweets.tweet_id = tweet_instance.tweet_id
    AND tweets.publish_date >= %(start_date)s AND tweets.publish_date < %(end_date)s
    AND tweets.is_retweet != %(hide_value)s
    GROUP BY authors.author_name
    ORDER BY '''+sort_by+''' DESC;'''
    try:
        cursor.execute(query, ({ 'start_date':start_date, 'end_date':end_date, 'hide_value':hide_value}))
    except Exception as e:
        print(e)
        exit()
    return cursor

def json_output_user_rankings( sort_metric = 'Followers', start_date = '2000-01-01', end_date = '2022-01-01', hide_original_tweets = False, hide_retweets = False):
    '''returns the JSON output contaning the data from top performing bots'''
    cursor = user_rankings_sql(sort_metric, start_date, end_date, hide_original_tweets, hide_retweets)
    output_list = []
    for row in cursor:
        row_dictionary = {}
        row_dictionary["author_name"] = row[0]
        row_dictionary["sorting_data"] = row[1]
        output_list.append(row_dictionary)
    return json.dumps(output_list)

def output_followers_over_time_sql(account_name):
    '''sql for getting the changes in follower count to graph'''
    cursor = get_connection().cursor()
    query = '''SELECT DISTINCT tweet_instance.followers, tweets.publish_date
    FROM tweets, authors, tweet_instance
    WHERE authors.external_author_id = tweet_instance.author_id
    AND tweets.tweet_id = tweet_instance.tweet_id
    AND authors.author_name LIKE %(input_query)s
    ORDER BY tweets.publish_date;'''
    try:
        cursor.execute(query, ({'input_query':'%'+account_name+'%'}))
    except Exception as e:
        print(e)
        exit()
    return cursor

def json_output_followers_over_time(query):
    '''returns the JSON output contaning the data from the followers_over_time sql call'''
    cursor = output_followers_over_time_sql(query)
    output_list = []
    for row in cursor:
        row_dictionary = {}
        row_dictionary["y"] = row[0]
        row_dictionary["x"] = row[1]
        output_list.append(row_dictionary)
    return json.dumps(output_list)


def output_random_tweet():
    '''sql for getting a random tweet'''
    cursor = get_connection().cursor()
    query = '''SELECT authors.author_name, tweet_instance.followers, tweets.publish_date, 
    tweets.tweet_content
    FROM tweets, authors, tweet_instance
    WHERE authors.external_author_id = tweet_instance.author_id
    AND tweets.tweet_id = tweet_instance.tweet_id
    ORDER BY RANDOM() LIMIT 1;'''
    try:
        cursor.execute(query)
    except Exception as e: 
        print(e)
        exit()
    return cursor

def json_output_random_tweet():
    '''returns the JSON output contaning the data from the random_tweet sql call'''
    cursor = output_random_tweet()
    output_list = []
    for row in cursor:
        row_dictionary = {}
        row_dictionary["author_name"] = row[0]
        row_dictionary["followers"] = row[1]
        row_dictionary["date"] = row[2]
        row_dictionary["content"] = row[3]
        output_list.append(row_dictionary)
    return json.dumps(output_list)