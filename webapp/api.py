'''
    api.py
    Simon Hempel-Costello, 25 April 2016
    Updated 8 November 2021

    Tiny Flask API to support the tiny books web application.
'''
import sys
import flask
import sql_interface

api = flask.Blueprint('api', __name__)

@api.route('/search/input/<search_query>')
def get_books_for_author(search_query):
    return sql_interface.json_output_tweet_search(search_query)
