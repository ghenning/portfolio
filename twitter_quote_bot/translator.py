import requests
from auth_key import KEY

class Translator:
	# a class that uses the DeepL API to translate text
	def __init__(self):
		self.key = KEY
		# DeepL API translation endpoint
		self.translate_endpoint = "https://api-free.deepl.com/v2/translate"
		# DeepL API usage limit endpoint
		self.usage_endpoint = "https://api-free.deepl.com/v2/usage"
		# set up the json for translation requests
		self.jason = {
			'auth_key': self.key,
			'text': "",
			'target_lang': "",
			'source_lang': "",
			'preserve_formatting': "1",
			'split_sentences': "nonewlines"
		}
		# set up the json for usage requests
		self.header = {
			'auth_key': self.key
		}

	def translate(self,TEXT,SOURCE_LANG,TARGET_LANG):
		# translate text from source lang to target lang
		self.jason['text'] = TEXT
		self.jason['target_lang'] = TARGET_LANG
		self.jason['source_lang'] = SOURCE_LANG
		tmp_response = requests.post(url=self.translate_endpoint,params=self.jason)
		tmp_response.raise_for_status()
		# parse the API response and return it
		return tmp_response.json()['translations'][0]['text']	

	def check_usage(self):
		# free account has a limited number of characters to translate
		# use this to check the usage status
		tmp_response = requests.get(url=self.usage_endpoint,params=self.header)
		tmp_response.raise_for_status()
		print("Deepl monthly character count: {}".format(tmp_response.json()))	
