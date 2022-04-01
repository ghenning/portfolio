#import string
# make a dictionary of letters/morse
letters = {	'a':'.-',
			'b':'-...',
			'c':'-.-.',
			'd':'-..',
			'e':'.',
			'f':'..-.',
			'g':'--.',
			'h':'....',
			'i':'..',
			'j':'.---',
			'k':'-.-',
			'l':'.-..',
			'm':'--',
			'n':'-.',
			'o':'---',
			'p':'.--.',
			'q':'--.-',
			'r':'.-.',
			's':'...',
			't':'-',
			'u':'..-',
			'v':'...-',
			'w':'.--',
			'x':'-..-',
			'y':'-.--',
			'z':'--..',
			'1':'.----',
			'2':'..---',
			'3':'...--',
			'4':'....-',
			'5':'.....',
			'6':'-....',
			'7':'--...',
			'8':'---..',
			'9':'----.',
			'0':'-----',
			'/':'/'}

# make alphabet list
#letters = list(string.ascii_lowercase)
#letters.append('/')

#the_dict = {k:v for k,v in zip(letters,morse)}

def text_to_morse(TEXT):
	""" takes a text and prints the morse equivalent """
	TEXT = TEXT.replace(" ","/") # split words with a '/'
	# looks through the input text, if in alphabet/numbers it grabs the morse equiv.
	translated = [letters.get(letter) for letter in TEXT if letter in letters.keys()]
	print(" ".join(translated)) # a space ' ' between letters, '/' between words

if __name__ == "__main__":
	print("Let's translate some text to morse.")
	# keep translating until you're bored
	keep_morsing = 1
	while keep_morsing:
		# user input text to translate
		to_translate = input("enter your text here:\n").lower()
		# morse-fy it
		text_to_morse(to_translate)
		# keep morsing or not
		tmp_q = input("would you like to keep going? (Y/N)\n").lower()
		if tmp_q != 'y':
			keep_morsing = 0	
