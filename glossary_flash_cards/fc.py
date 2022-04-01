import tkinter as tk
import os
import pandas as pd
import numpy as np
import glob

### constants

CSVs = glob.glob("word_banks/*.csv")
CSVs = [x for x in CSVs if "_known.csv" not in x]
CSVs = [os.path.splitext(os.path.basename(x))[0] for x in CSVs]
CSVs.sort()

BG_COLOR = "#B1DDC6"
BLK = "#000000"
WHT = "#FFFFFF"
FNT1 = ("Futura",22,"italic")
FNT2 = ("Futura",26,"bold")
FNT3 = ("Futura",12,"normal")
FNT4 = ("Futura",14,"bold")

class StartScreen:
	def __init__(self,master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.frame.config(padx=50,pady=50,bg=BG_COLOR)
		self.widgets()

	def widgets(self):

		# labels
		self.title_label = tk.Label(self.frame,
			text="Tsipa's German Flash Cards",
			font=FNT4,padx=20,pady=20,bg=BG_COLOR)
		self.lvl_label = tk.Label(self.frame,
			text="Choose a level",
			font=FNT3,padx=20,pady=5,bg=BG_COLOR)
		self.nword_label = tk.Label(self.frame,
			text="Choose number of words",
			font=FNT3,padx=20,pady=5,bg=BG_COLOR)

		# start/exit buttons
		self.button = tk.Button(self.frame,text="Start",
				width=20,command = self.start_game,
				font=FNT3,pady=10)
		self.quitButton = tk.Button(self.frame,text="Exit",
				width=20,command = self.close_window,
				font=FNT3,pady=10)

		# drop down option 1
		self.OptList = CSVs
		self.var = tk.StringVar(self.frame)
		self.var.set(self.OptList[0])
		self.opt = tk.OptionMenu(self.frame,self.var,*self.OptList)
		self.opt.config(width=30,font=FNT3,pady=10)

		# drop down option 2
		self.NWords = list(range(10,51,10))
		self.var2 = tk.StringVar(self.frame)
		self.var2.set(self.NWords[0])
		self.opt2 = tk.OptionMenu(self.frame,self.var2,*self.NWords)
		self.opt2.config(width=30,font=FNT3,pady=10)

		# place widgets on frame 
		self.frame.grid()
		self.title_label.grid(row=0,column=0)
		self.lvl_label.grid(row=1,column=0)
		self.nword_label.grid(row=3,column=0)
		self.opt.grid(row=2,column=0)
		self.opt2.grid(row=4,column=0)
		self.button.grid(row=5,column=0,pady=(10,0))
		self.quitButton.grid(row=6,column=0,pady=(10,0))

	def start_game(self):

		# get level and number of words
		self.level = self.var.get()
		self.num_words = self.var2.get()

		# grab the word bank csvs
		self.full_lib = os.path.join("word_banks",
			"{}.csv".format(self.level))
		self.known_lib = os.path.join("word_banks",
			"{}_known.csv".format(self.level))

		# go to the game screen
		self.swap_window(self.full_lib,self.known_lib,self.num_words)

	def swap_window(self,*args):
		# args are path to full_lib and known lib, and number of words
		self.frame.destroy()
		self.app = GameScreen(self.master,args)
		
	def close_window(self):
		self.master.destroy()

class GameScreen:
	def __init__(self,master,*args):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.frame.config(padx=50,pady=50,bg=BG_COLOR)
		self.state = False # 0 for german, 1 for english
		self.full_lib = np.squeeze(args)[0]
		self.known_lib = np.squeeze(args)[1]
		self.num_words = int(np.squeeze(args)[2])
		self.FNT2 = FNT2
		self.widgets()
		self.set_up_dbs()
		self.gen_card()

	def widgets(self):

		# back/exit buttons
		self.quitButton = tk.Button(self.frame,text="Exit",
				width=20,command = self.close_window,font=FNT3)
		self.button = tk.Button(self.frame,text="Back",
				width=20,command = self.swap_window,font=FNT3)

		# cross
		self.ex_img = tk.PhotoImage(file='images/wrong.png')
		self.ex = tk.Button(self.frame,image=self.ex_img,
			highlightthickness=0,command=self.red_light)

		# check
		self.ya_img = tk.PhotoImage(file='images/right.png')
		self.ya = tk.Button(self.frame,image=self.ya_img,
			highlightthickness=0,command=self.green_light)

		# flip
		self.flip_img = tk.PhotoImage(file='images/flip.png')
		self.flip = tk.Button(self.frame,image=self.flip_img,
			highlightthickness=0,command=self.flip_card)

		# flash card
		#self.flash_card = tk.Canvas(self.frame,width=800,height=526,
		#	bg=BG_COLOR,highlightthickness=0)
		self.flash_card = tk.Canvas(self.frame,width=640,height=420,
			bg=BG_COLOR,highlightthickness=0)
		self.img = tk.PhotoImage(file='images/card_front_s.png')
		self.img2 = tk.PhotoImage(file='images/card_back_s.png')
		#self.fc_img = self.flash_card.create_image(400,263,image=self.img)
		self.fc_img = self.flash_card.create_image(320,210,image=self.img)
		#self.fc1 = self.flash_card.create_text(400,150,
		#	text="German",font=FNT1,fill=BLK)
		#self.fc2 = self.flash_card.create_text(400,263,
		#	text="Word",font=FNT2,fill=BLK)
		self.fc1 = self.flash_card.create_text(320,100,
			text="German",font=FNT1,fill=BLK,width=590)
		self.fc2 = self.flash_card.create_text(320,210,
			text="Word",font=FNT2,fill=BLK,width=590)

		# place it
		self.frame.grid()
		self.button.grid(row=0,column=2)
		self.quitButton.grid(row=0,column=0)
		self.flash_card.grid(row=1,column=0,columnspan=3,pady=(20,0))
		self.ex.grid(row=2,column=0)
		self.ya.grid(row=2,column=2)
		self.flip.grid(row=2,column=1)

	def flip_card(self):
		# flip card from one language to the other
		if self.state:
			self.flash_card.itemconfig(self.fc1,text="English",
				font=FNT1,fill=WHT)
			self.flash_card.itemconfig(self.fc2,text=self.word_english,
				font=self.FNT2,fill=WHT)
			self.flash_card.itemconfig(self.fc_img,image=self.img2)
			self.state = not self.state
		else:
			self.flash_card.itemconfig(self.fc1,text="German",
				font=FNT1,fill=BLK)
			self.flash_card.itemconfig(self.fc2,text=self.word_german,
				font=self.FNT2,fill=BLK)
			self.flash_card.itemconfig(self.fc_img,image=self.img)
			self.state = not self.state

	def set_up_dbs(self):
		# making dfs from csvs
		self.full_df = pd.read_csv(self.full_lib)
		try:
			self.known_df = pd.read_csv(self.known_lib)
		except FileNotFoundError:
			with open(self.known_lib,'w') as f:
				f.write("German,English\n")
			self.known_df = pd.read_csv(self.known_lib)
		# concat dfs and then drop duplicates,
		#	that should yield full_lib - known_lib
		self.full_df = pd.concat([self.full_df,self.known_df],
			axis=0,ignore_index=True).drop_duplicates(keep=False)

		# split all words/known words in 80/20
		self.N1 = int(.8*self.num_words)
		self.N2 = int(.2*self.num_words)

		# check if there are enough words in known words
		if self.N2 > len(self.known_df):
			self.N2 = len(self.known_df)
			self.N1 = self.num_words - self.N2
		# check if there are any unknown words left,
		#	otherwise just pull all from known_lib
		if self.N1 > len(self.full_df):
			self.N1 = len(self.full_df)
			self.N2 = self.num_words - self.N1

		# grab samples from dfs and merge into game df
		tmp_full = self.full_df.sample(min(self.N1,len(self.full_df)))
		tmp_known = self.known_df.sample(min(self.N2,len(self.known_df)))
		self.df = pd.concat([tmp_full,tmp_known],
			axis=0,ignore_index=True)
			
	def gen_card(self):
		# generate a new card
		# if there are words left in the game df, continue game
		# else, give congratulations
		if len(self.df) > 0:
			self.word = self.df.sample()
			self.word_english = self.word['English'].values[0]
			self.word_german = self.word['German'].values[0]
			self.flip_card()
		else:
			self.word = pd.DataFrame(
				[["Glückwünsche!\nTo reset,click back. To exit, click exit.",
				"Congratulations!\nTo reset,click back. To exit, click exit."]],
				columns=['German','English'])
			self.word_english = self.word['English'].values[0]
			self.word_german = self.word['German'].values[0]
			self.FNT2 = FNT4
			self.flip_card()

	def green_light(self):
		# if you've learned the word, add it to the known word df
		# add word to known_lib if it is not there
		if self.known_df[self.known_df['German'].str.contains(self.word_german)].empty:
			self.known_df = pd.concat([self.known_df,self.word],
				axis=0,ignore_index=True)
			# write out known_lib
			self.update_known()

		# drop the word from the game df
		tmp_idx = self.df.index[self.df['German']==self.word_german]
		self.df.drop(tmp_idx,axis=0,inplace=True)

		# set to german and generate a new card
		self.state = 0
		self.gen_card()

	def red_light(self):
		# don't know the word, it will stay in the game
		# get a new word
		self.state = 0
		self.gen_card()

	def update_known(self):
		# if statement there so congratulations message isn't added
		if len(self.df) > 0:
			self.known_df.to_csv(self.known_lib,index=False)

	def close_window(self):
		self.master.destroy()

	def swap_window(self):
		self.frame.destroy()
		self.app = StartScreen(self.master)

def main():
	root = tk.Tk()
	root.title("Flash Cards")
	app = StartScreen(root)
	root.mainloop()

if __name__=="__main__":
	main()
