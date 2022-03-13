import requests
import random

class Quoter:
	# a class that grabs random quotes and scrambles them

	def __init__(self):
		# quote API endpoint
		self.endpoint = "https://zenquotes.io/api/random"
		self.quote = ""
		self.author = ""
		self.scrambled_quote = ""

	def grab_quote(self):
		# grab a random quote
		tmp_response = requests.get(url=self.endpoint)
		# parse the API response
		tmp_data = tmp_response.json()[0]
		self.quote = tmp_data['q']
		self.author = tmp_data['a']

	def shuffle_quote(self):
		# shuffle the quote
		tmp_list = [word for word in self.quote.split()]
		random.shuffle(tmp_list)
		self.scrambled_quote = " ".join(tmp_list)
