from flask import Flask, jsonify, request, render_template, json
import TwitterApp

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search_tweets():
    screen_name = request.args.get('screenName')
    search_text = request.args.get('searchText')
    print screen_name, search_text
    tweet_app = TwitterApp.TwitterApp()
    result = tweet_app.search_tweets(screen_name, search_text)
    print "result  ", result

    return jsonify({'result': result})
    #return render_template("SearchResult.html", result=jsonify({'result': result}))
    # return "Hello World"


@app.route('/followers')
def get_followers():
    screen_name = request.args.get('screen_name')
    tweet_app = TwitterApp.TwitterApp()
    return jsonify(tweet_app.get_user_followers(screen_name))


@app.route("/get_tweets")
def get_tweets():
    screen_name = request.args.get('screen_name')
    tweet_app = TwitterApp.TwitterApp()
    return jsonify(tweet_app.tweets(screen_name))


@app.route("/")
def main():
    return render_template('Search.html')


if __name__ == "__main__":
    app.run()
