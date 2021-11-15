'''
    api.py
    Simon Hempel-Costello, Lev Schuster
    25 April 2016
'''
import sys
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
@api.route('/search/input/<search_query>')
def get_tweets_from_input(search_query):
    return sql_interface.json_output_tweet_search(search_query)
@api.route('/rankings/input/<input_json>')
def get_users_by_ranking(input_json):
    query = json.loads(input_json)
    input_start_date = query['start_date']
    input_end_date = query['end_date']
    input_hide_original_tweets = query['hide_original_tweets']
    input_hide_retweets = query['hide_retweets']
    return sql_interface.json_output_user_rankings(start_date=input_start_date, end_date=input_end_date, hide_original_tweets=input_hide_original_tweets, hide_retweets=input_hide_retweets)