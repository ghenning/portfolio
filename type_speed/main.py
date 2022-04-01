import tkinter as tk
import random
import requests
import time

# setting up some fonts and colors
BG_COLOR = '#0382A8'
BG_COLOR2 = '#9AE0F5'
FNT1 = ("Ubuntu",22,"bold")
FNT2 = ("Ubuntu",18,"normal")
FNT3 = ("Ubuntu",14,"italic")
FNT4 = ("Ubuntu",16,"bold")

class MainScreen():

	def __init__(self,master):
		# setup the tkinter frame
		self.master = master
		self.frame = tk.Frame(self.master)
		# set frame padding and background color
		self.frame.config(padx=50,pady=50,bg=BG_COLOR)
		# grab word list
		self.collect_words()
		# grab first word
		self.get_new_word()
		# starting counters
		self.correct_words = 0
		self.wrong_words = 0
		self.words_per_minute = 0
		# word counter is off until user starts typing
		self.game_on = 0
		# set up the tkinter widgets
		self.widgets()

	def widgets(self):
		""" set up all the tkinter widgets """
		# the title label
		self.title_label = tk.Label(self.frame,
			text="Speed typing test",
			font = FNT1,
			padx = 20,
			pady = 20,
			bg = BG_COLOR,
			fg = 'white')

		# instructions/status label
		self.instruct_var = tk.StringVar()
		self.instruct_var.set("Start typing in the box below to start, press spacebar to get next word")
		self.instructions = tk.Label(self.frame,
			textvariable = self.instruct_var,
			font = FNT3,
			bg = BG_COLOR,
			fg = 'white',
			wraplength=250)

		# the word to write
		self.target_word = tk.StringVar()
		self.target_word.set(self.current_word)
		self.to_write = tk.Label(self.frame,
			textvariable=self.target_word,
			font = FNT2,
			bg = BG_COLOR,
			fg = 'white')

		# entry box for typing
		self.writing_box = tk.Entry(self.frame,
			font = FNT2,
			bg = BG_COLOR2)

		# set the entrybox text as a fetchable variable
		self.content = tk.StringVar()
		self.content.set('')
		self.writing_box['textvariable'] = self.content

		# pressing any key in the entrybox will start the game
		self.writing_box.bind('<KeyPress>',self.start)
		# space checks if user typed correctly and will fetch a new word
		self.writing_box.bind('<space>',self.check_word)

		# exit button
		self.xit_btn = tk.Button(self.frame,text='Exit',
			command=self.kill_me,font=FNT2)
	
		# reset button
		self.rst_btn = tk.Button(self.frame,text='Restart',
			command=self.reset,font=FNT2)

		# correct/incorrect words typed counter
		self.word_label_var = tk.StringVar()
		self.word_label_var.set("correct/incorrect: {}/{}".format(self.correct_words,self.wrong_words))
		self.wpm_label_var = tk.StringVar()

		# words per minute counter
		self.wpm_label_var.set("WPM: {}".format(self.words_per_minute))
		self.word_label = tk.Label(self.frame,
			textvariable=self.word_label_var,
			font = FNT4,
			bg = BG_COLOR,
			fg = 'white')
		self.wpm_label = tk.Label(self.frame,
			textvariable = self.wpm_label_var,
			font = FNT4,
			bg = BG_COLOR,
			fg = 'white')

		# place the widgets on the tkinter frame
		self.frame.grid()
		self.title_label.grid(row=0,column=0,columnspan=2,pady=20)
		self.writing_box.grid(row=3,column=0,columnspan=2,pady=10)
		self.to_write.grid(row=2,column=0,columnspan=2,pady=10)
		self.instructions.grid(row=1,column=0,columnspan=2,pady=10)
		self.word_label.grid(row=4,column=0,columnspan=2,pady=10)
		self.wpm_label.grid(row=5,column=0,columnspan=2,pady=10)
		self.rst_btn.grid(row=6,column=0,pady=10)
		self.xit_btn.grid(row=6,column=1,pady=10)

	def check_word(self,event):
		""" check if the typed word matches target and fetch a new word """
		if self.game_on:
			if self.content.get().strip() == self.current_word:
				self.correct_words += 1
			else:
				self.wrong_words += 1
			# get a new word
			self.get_new_word()
			# update the counter label
			self.word_label_var.set("correct/incorrect: {}/{}".format(self.correct_words,self.wrong_words))
			self.target_word.set(self.current_word)
			# clear the input box
			self.writing_box.delete(0,tk.END)

	def collect_words(self):
		""" grab word list from a random word API """
		response = requests.get("https://random-word-api.herokuapp.com/word?number=400")
		tmp_words = response.json()
		# only grab words with 7 or less letters
		self.words = [x for x in tmp_words if len(x)<=7]

	def get_new_word(self):
		""" grab a random word from the word list """
		self.current_word = random.choice(self.words)

	def start(self,event):
		""" start the game """
		if not self.game_on:
			self.game_on = 1
			# change instruction text
			self.instruct_var.set("Keep writing!")
			# set timer to 30 seconds
			self.timing(30)

	def timing(self,count):
		""" count down until the game ends """
		if count >= 0:
			self.master.after(1000,self.timing,count-1)
			# add time left to the instruction text
			self.instruct_var.set("Keep writing! ({})".format(count))
		else:
			# disable and destroy the entry box
			self.writing_box['state'] = 'disabled'
			self.writing_box.destroy()
			# destroy the target word box
			self.to_write.destroy()
			# sleep for a tiny bit so you can't accidentally restart game
			time.sleep(.2)
			self.game_on = 0
			self.instruct_var.set("Done!")
			# print final results
			self.word_label_var.set("correct/incorrect: {}/{}".format(self.correct_words,self.wrong_words))
			self.words_per_minute = self.correct_words * 2
			self.wpm_label_var.set("WPM: {:.1f}".format(self.words_per_minute))

	def reset(self):
		""" reset the game """
		# get a new word list and a new starting word
		self.collect_words()
		self.get_new_word()
		# destroy all widgets
		for widget in self.frame.winfo_children():
			widget.destroy()
		# reset counters
		self.correct_words = 0
		self.wrong_words = 0
		self.words_per_minute = 0
		# reset widgets
		self.widgets()

	def kill_me(self):
		""" exit """
		self.master.destroy()

def main():
	root = tk.Tk()
	root.title("Typing speed test")
	app = MainScreen(root)
	root.mainloop()

if __name__ == "__main__":
	main()
