'''
    app.py
    Simon Hempel-Costello, Lev Schuster
    25 April 2016
'''
import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/') 
def home():
    return flask.render_template('index.html')
@app.route('/index.html') 
def index_page():
    return flask.render_template('index.html')
@app.route('/search') 
def search():
    return flask.render_template('search.html')
@app.route('/wordcloud') 
def word_cloud():
    return flask.render_template('word-cloud.html')
@app.route('/about') 
def about():
    return flask.render_template('about.html') #why do we have two about pages?
@app.route('/about') 
def about_page():
    return flask.render_template('about.html')
@app.route('/im_feeling_lucky') 
def im_feeling_lucky():
    return flask.render_template('im-feeling-lucky.html')
@app.route('/rankings') 
def rankings():
    return flask.render_template('rankings.html')     
@app.route('/tweet') 
def tweet():
    return flask.render_template('tweet.html')    
@app.route('/follower_chart/<account_id>')
def graph_account(account_id):
    return flask.render_template('follower-chart.html')
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A database hosting tweets and associated data from Clemsons social media listener, including API & DB')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
