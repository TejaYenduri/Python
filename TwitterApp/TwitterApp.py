import json
import ConfigParser
from twython import Twython


class TwitterApp:
	def __init__(self):
		config = ConfigParser.SafeConfigParser()
		config.read('twitterauth.cfg')
		app_key = config.get('twitter','APP_KEY')
		app_secret = config.get('twitter','APP_SECRET')
		access_token = config.get('twitter','OAUTH_TOKEN')
		token_secret = config.get('twitter','TOKEN_SECRET')
		self.twitter = Twython(app_key, app_secret, access_token, token_secret)

	def tweets(self, screen_name):
		list_of_tweets=[]
		result = self.twitter.get_user_timeline(screen_name=screen_name,count=10)
		list_of_tweets=[i['text'] for i in result]
		return list_of_tweets
		
	def search_tweets(self, screenName, searchText):
		result = self.twitter.get_user_timeline(screen_name='MakeThunder',count=100)
		searchResult=[i['text'] for i in result if searchText in i['text']] 
		#data = json.dumps(searchResult)
		#print data
		return searchResult
		
	def get_user_followers(self, screenName):
		followersData = self.twitter.get_followers_list(screen_name=screenName, count=15)
		followerNames = [i["screen_name"]for i in followersData["users"]] 
		#followers = json.dumps(followerNames)
		#print followers
		return followerNames
		
tweetapp = TwitterApp()
#tweetapp.search_tweets('MakeThunder','Load')
tweetapp.tweets('MakeThunder')
#tweetapp.get_user_followers('MakeThunder')