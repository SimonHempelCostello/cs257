'''
    api.py
    Simon Hempel-Costello, Lev Schuster
    25 April 2016
'''
import sys
import flask
import sql_interface

api = flask.Blueprint('api', __name__)

@api.route('/search/input/<search_query>')
def get_books_for_author(search_query):
    return sql_interface.json_output_tweet_search(search_query)
