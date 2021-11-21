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
    '''some necessary date sanitation to deal with the dates ouput by the javascript'''
    input_start_date = query['start_date'].replace('-0','-')
    input_start_date = input_start_date.replace('-','/')
    input_end_date = query['end_date'].replace('-0','-')
    input_end_date = input_end_date.replace('-','/')
    input_sorting_metric = query['sort_metric']
    input_search_query = query['search_string']
    return sql_interface.json_output_tweet_search(search_query= input_search_query, sorting_metric = input_sorting_metric, end_date = input_end_date, start_date= input_start_date)
@api.route('/help/')
def get_help():
    help_text = open('templates/help.txt').read()
    return flask.Response(help_text, mimetype='text/plain')
@api.route('/rankings/input/<input_json>')
def get_users_by_ranking(input_json):
    query = json.loads(input_json)
    '''some necessary date sanitation to deal with the dates ouput by the javascript'''
    input_start_date = query['start_date'].replace('-0','-')
    input_start_date = input_start_date.replace('-','/')
    input_end_date = query['end_date'].replace('-0','-')
    input_end_date = input_end_date.replace('-','/')
    input_hide_original_tweets = query['hide_original_tweets']
    input_hide_retweets = query['hide_retweets']
    input_sorting_metric = query['sort_metric']
    return sql_interface.json_output_user_rankings(sort_metric = input_sorting_metric,start_date=input_start_date, end_date=input_end_date, hide_original_tweets=input_hide_original_tweets, hide_retweets=input_hide_retweets)