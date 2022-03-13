import requests
from auth_key import TW_API_KEY, TW_API_KEY_SECRET,TW_BEAR,TW_ACCESS_SECRET,TW_ACCESS_TOKEN
import tweepy

class Tweeter:
	# a class that sends tweets
	# methods for the self.client can be added to
	#     e.g. delete tweet, retweet, like, ...
	def __init__(self):
		# all the keys/tokens/secrets for the twitter/twitter app
		self.bear = TW_BEAR
		self.cons_key = TW_API_KEY
		self.cons_sec = TW_API_KEY_SECRET
		self.access_token = TW_ACCESS_TOKEN
		self.access_secret = TW_ACCESS_SECRET
		# set up the client that talks to the API
		self.client = tweepy.Client(bearer_token=self.bear,
				consumer_key=self.cons_key,
				consumer_secret=self.cons_sec,
				access_token=self.access_token,
				access_token_secret=self.access_secret)

	def tweet(self,MSG):
		# post tweet containing MSG
		self.client.create_tweet(text=MSG)

