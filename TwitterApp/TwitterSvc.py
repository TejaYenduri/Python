from flask import Flask, jsonify, request, render_template

import TwitterApp

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search_tweets():
    screen_name = request.args.get('screenName')
    search_text = request.args.get('searchText')
    tweet_app = TwitterApp.TwitterApp()
    result = tweet_app.search_tweets(screen_name, search_text)
    return jsonify({'result': result})


@app.route('/followers')
def get_followers():
    screen_name = request.args.get('screenName')
    tweet_app = TwitterApp.TwitterApp()
    return jsonify(tweet_app.get_user_followers(screen_name))


@app.route("/get_tweets")
def get_tweets():
    screen_name = request.args.get('screenName')
    tweet_app = TwitterApp.TwitterApp()
    result = tweet_app.tweets(screen_name)
    return jsonify({'result': result})


@app.route("/tweets")
def tweets_url():
    return render_template("Tweets.html")


@app.route("/user_followers")
def user_followers():
    return render_template("Followers.html")


@app.route("/")
def main():
    return render_template('Search.html')


if __name__ == "__main__":
    app.run()
