import ConfigParser

from twython import Twython
import json


class TwitterApp:
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.read('twitterauth.cfg')
        app_key = config.get('twitter', 'APP_KEY')
        app_secret = config.get('twitter', 'APP_SECRET')
        access_token = config.get('twitter', 'OAUTH_TOKEN')
        token_secret = config.get('twitter', 'TOKEN_SECRET')
        self.twitter = Twython(app_key, app_secret, access_token, token_secret)

    def tweets(self, screen_name):
        result = self.twitter.get_user_timeline(screen_name=screen_name, count=10)
        list_of_tweets = [i['text'] for i in result]
        return json.dumps(list_of_tweets)

    def search_tweets(self, screen_name, search_text):
        result = self.twitter.get_user_timeline(screen_name=screen_name, count=100)
        search_result = [i['text'] for i in result if search_text in i['text']]
        #data = json.dumps(search_result)
        # print data
        #return data
        return search_result

    def get_user_followers(self, screen_name):
        followers_data = self.twitter.get_followers_list(screen_name=screen_name, count=15)
        follower_names = [i["screen_name"] for i in followers_data["users"]]
        # followers = json.dumps(followerNames)
        # print followers
        return follower_names


tweet_app = TwitterApp()
# tweetapp.search_tweets('MakeThunder','Load')
tweet_app.tweets('MakeThunder')
# tweetapp.get_user_followers('MakeThunder')
