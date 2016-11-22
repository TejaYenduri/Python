import ConfigParser

from twython import Twython, TwythonError
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
        list_of_tweets=[]
        try:
            result = self.twitter.get_user_timeline(screen_name=screen_name, count=10)
            list_of_tweets = [i['text'] for i in result]
        except TwythonError as err:
            message = err.message
            print message


        return list_of_tweets

    def search_tweets(self, screen_name, search_text):
        ''' function to search given text in user tweets '''
        search_result = []
        try:
            result = self.twitter.get_user_timeline(screen_name=screen_name, count=100)
            search_result = [i['text'] for i in result if search_text in i['text']]
        #data = json.dumps(search_result)
        # print data
        #return data
        except TwythonError as err:
            message = err.message
            print message
        return search_result

    def get_user_followers(self, screen_name):
        ''' function to get followers for given user '''
        follower_names = []
        try:
            followers_data = self.twitter.get_followers_list(screen_name=screen_name, count=15)
            follower_names = [i["screen_name"] for i in followers_data["users"]]
        # followers = json.dumps(followerNames)
        # print followers
        except TwythonError as err:
            message = err.message
            print message
        return follower_names

    def common_followers(self, user_1, user_2):
        ''' function to get common followers of two users '''
        common_followers = []
        try:
            user1_data = self.twitter.get_followers_list(screen_name=user_1, count=100)
            user2_data = self.twitter.get_followers_list(screen_name=user_2, count=100)
            user1_followers = [i["screen_name"] for i in user1_data["users"]]
            user2_followers = [i["screen_name"] for i in user2_data["users"]]       
            for follower in user1_followers:
                if follower in user2_followers:
                    common_followers.append(follower)
            print json.dumps(common_followers)
        except TwythonError as err:
            message = err.message
            print message
        return common_followers






tweet_app = TwitterApp()
# tweetapp.search_tweets('MakeThunder','Load')
#tweet_app.tweets('MakeThunder')
# tweetapp.get_user_followers('MakeThunder')
tweet_app.common_followers("TwitterEng", "twitterapi")
