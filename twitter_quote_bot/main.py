from quoter import Quoter
from translator import Translator
from tweeter import Tweeter
import random

def main():
	# create a quote object
	quote_object = Quoter()
	# grab a random quote from API
	quote_object.grab_quote()
	# shuffle the quote around
	quote_object.shuffle_quote()
	# create a translator object
	translator_object = Translator()
	# languages to transform from
	source_langs = ['EN','JA','DE']
	# languages to transform to
	target_langs = ['JA','DE','EN-GB']
	# some phrases to add at the end
	some_flair = ['I think','sort of','approx','maybe','possibly']
	# grab the scrambled quote
	tmp_translation = quote_object.scrambled_quote
	# send the quote through a series of translations
	for sl,tl in zip(source_langs,target_langs):
		tmp_translation = translator_object.translate(tmp_translation,sl,tl)
	# compose the tweet
	msg_to_tweet = "\"{}\" - {} ({})".format(tmp_translation,
		quote_object.author,random.choice(some_flair))
	# create a twitter object
	twat = Tweeter()
	# tweet it
	twat.tweet(msg_to_tweet)

	# check usage limit
	#translator_object.check_usage()

if __name__ == "__main__":
	main()
