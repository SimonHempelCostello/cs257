'''
    api.py
    Simon Hempel-Costello, Lev Schuster
    13 Noverber 2021
'''

import flask
import sql_interface
import json

api = flask.Blueprint('api', __name__)

@api.route('/random-tweet/')
def random_tweet():
    return sql_interface.json_output_random_tweet()

@api.route('/follower-chart/input/<search_query>')
def get_folloer_for_a_user(search_query):
    return sql_interface.json_output_followers_over_time(search_query)

@api.route('/search/input/<search_query_json>')
def get_tweets_from_input(search_query_json):
    query = json.loads(search_query_json)
    date=sanitize(query)
    return sql_interface.json_output_tweet_search(search_query= query['search_string'], sorting_metric = date['sorting_metric'], end_date = date['end'], start_date= date['start'])

@api.route('/help/')
def get_help():
    help_text = open('templates/help.txt').read()
    return flask.Response(help_text, mimetype='text/plain')


@api.route('/rankings/input/<input_json>')
def get_users_by_ranking(input_json):
    query = json.loads(input_json)
    date=sanitize(query)
    return sql_interface.json_output_user_rankings(sort_metric = date['sorting_metric'],start_date=date['start'], end_date=date['end'])

def sanitize(query):
    '''some necessary date sanitation to deal with the dates ouput by the javascript'''
    sanitized = {}

    input_start_date = query['start_date'].replace('-0','-')
    sanitized['start'] = input_start_date.replace('-','/')

    input_end_date = query['end_date'].replace('-0','-')
    sanitized['end'] = input_end_date.replace('-','/')

    sanitized['sorting_metric'] = query['sort_metric']

    return sanitized