import requests
import numpy as np

from auth_key import rapidapi_key

class movie_caller:
	def __init__(self):
		self.auth_key = rapidapi_key
		self.host = "online-movie-database.p.rapidapi.com"
		self.pop_endpoint = "https://online-movie-database.p.rapidapi.com/title/v2/get-popular-movies-by-genre" 
		self.meta_endpoint = "https://online-movie-database.p.rapidapi.com/title/get-meta-data"

	def get_top_x(self,genre='adventure',limit=100):
		qstring = {"genre":genre,
			"limit":str(limit)}
		headers = {"X-RapidAPI-Key":self.auth_key,
			"X-RapidAPI-Host": self.host}	
		response = requests.request("GET",
			self.pop_endpoint,
			headers=headers,
			params=qstring)

		return np.random.choice(response.json()).split('/')[-2]

	def get_meat(self,movie_id):
		qstring = {"ids":movie_id,
			"region":"US"}
		headers = {"X-RapidAPI-Key":self.auth_key,
			"X-RapidAPI-Host": self.host}	
		response = requests.request("GET",
			self.meta_endpoint,
			headers=headers,
			params=qstring)

		res_title = response.json()[movie_id]['title']['title']
		res_year = response.json()[movie_id]['title']['year']
		try:
			res_runtime = response.json()[movie_id]['title']['runningTimeInMinutes']
		except KeyError:
			res_runtime = "N/A"
		try:
			res_poster = response.json()[movie_id]['title']['image']['url'] 
		except KeyError:
			res_poster = "N/A" 
		try:
			res_rate1 = response.json()[movie_id]['ratings']['rating']
		except KeyError:
			res_rate1 = "N/A"
		try:
			res_rate2 = response.json()[movie_id]['metacritic']['metaScore'] 
		except KeyError:
			res_rate2 = "N/A"
		res_genre = response.json()[movie_id]['genres']
		try:
			res_age = response.json()[movie_id]['certificate']
		except KeyError:
			res_age = "N/A"

		return [res_title,res_year,res_runtime,res_poster,res_rate1,
				res_rate2,res_genre,res_age]
