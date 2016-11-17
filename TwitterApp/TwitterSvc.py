from flask import Flask,jsonify,request

import TwitterApp
app = Flask(__name__)

@app.route('/search')
def search_tweets():
	screen_name = request.args.get('screen_name')
	search_text = request.args.get('search_text')
	tweetapp = TwitterApp.TwitterApp()
	return jsonify(tweetapp.search_tweets(screen_name,search_text))

@app.route('/followers')
def get_followers():
	screen_name = request.args.get('screen_name')
	tweetapp = TwitterApp.TwitterApp()
	return jsonify(tweetapp.get_user_followers(screen_name))

@app.route('/gettweets')
def get_tweets():
	screen_name = request.args.get('screen_name')
	tweetapp = TwitterApp.TwitterApp()
	return jsonify(tweetapp.tweets(screen_name))