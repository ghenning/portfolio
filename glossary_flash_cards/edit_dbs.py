import tkinter as tk
import os 
import pandas as pd
import glob

#constants
BG_COLOR = "#B1DDC6"
BLK = "#000000"
WHT = "#FFFFFF"

FNT1 = ("Futura",14,"bold")
FNT2 = ("Futura",12,"normal")

class EditScreen1:
	def __init__(self,master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.frame.config(padx=50,pady=50,bg=BG_COLOR)
		self.widgets()

	def widgets(self):
		
		#label
		self.head_label = tk.Label(self.frame,
			text="Database editing tool",
			font=FNT1,bg=BG_COLOR)

		# buttons
		self.quitButton = tk.Button(self.frame,text="Exit",
			command = self.close_window,
			font=FNT2,width = 15)

		self.editButton = tk.Button(self.frame,
			text="Add to existing",
			command = self.editDB,
			font=FNT2,width=15)

		self.newButton = tk.Button(self.frame,
			text="Create new",
			command = self.newDB,
			font=FNT2,width=15)

		# place things
		self.frame.grid()
		self.head_label.grid(row=0,column=0,pady=20)
		self.editButton.grid(row=1,column=0,pady=5)
		self.newButton.grid(row=2,column=0,pady=5)
		self.quitButton.grid(row=3,column=0,pady=5)

	def close_window(self):
		self.master.destroy()

	def editDB(self):
		self.edit_state = 0
		self.move_screens()

	def newDB(self):
		self.edit_state = 1
		self.move_screens()	

	def move_screens(self):
		self.frame.destroy()
		self.app = EditScreen2(self.master,self.edit_state)

class EditScreen2:
	def __init__(self,master,edit_state):
		self.master = master
		self.edit_state = edit_state
		self.frame = tk.Frame(self.master)
		self.frame.config(padx=50,pady=50,bg=BG_COLOR)
		self.grab_csvs()
		self.widgets()

	def grab_csvs(self):
		self.CSVs = glob.glob("word_banks/*.csv")
		self.CSVs = [x for x in self.CSVs if "_known.csv" not in x]
		self.CSVs = [os.path.splitext(os.path.basename(x))[0] for x in self.CSVs]
		self.CSVs.sort()

	def widgets(self):

		#labels
		self.head_label = tk.Label(self.frame,
			text="Database editing tool",
			font=FNT1,bg=BG_COLOR)

		# if edit mode
		## find CSV to edit
		# else new mode
		## write CSV to create
		self.csv_label = tk.Label(self.frame,
			font=FNT1,bg=BG_COLOR)
		if self.edit_state:
			self.csv_label.config(text="Name your new file")
		else:
			self.csv_label.config(text="Choose a file to add to")

		self.ger_label = tk.Label(self.frame,
			font=FNT2,bg=BG_COLOR,text="German input here:")
		self.eng_label = tk.Label(self.frame,
			font=FNT2,bg=BG_COLOR,text="English input here:")

		# back/exit buttons
		self.quitButton = tk.Button(self.frame,text="Exit",
			command = self.close_window,
			font=FNT2,width = 10)
		self.backButton = tk.Button(self.frame,text="Back",
			command = self.move_screens,
			font=FNT2,width=10)

		# submit button
		self.subButton = tk.Button(self.frame,text="Submit",
			command = self.submit,
			font=FNT1,width=10,
			bg='green',fg=WHT) 

		# clear button
		self.clearButton = tk.Button(self.frame,text="Clear",
			command = self.clear_it,
			font=FNT1,width=10,
			bg='red',fg=WHT)

		# if edit mode
		self.OptList = self.CSVs
		self.listvar = tk.StringVar(self.frame)
		self.listvar.set(self.OptList[0])	
		self.opt = tk.OptionMenu(self.frame,
			self.listvar,*self.OptList)
		self.opt.config(width=30,font=FNT2)

		# if new mode
		self.entry = tk.Entry(self.frame,width=30,font=FNT2)

		# text boxes
		self.ger_text = tk.Text(self.frame,height=5,width=30,font=FNT1)
		self.eng_text = tk.Text(self.frame,height=5,width=30,font=FNT1)

		# place things
		self.frame.grid()
		self.head_label.grid(row=1,column=0,pady=10,columnspan=2)
		self.csv_label.grid(row=2,column=0,pady=5,columnspan=2)
		if self.edit_state:
			self.entry.grid(row=3,column=0,pady=5,columnspan=2)
			self.entry.focus()
		else:
			self.opt.grid(row=3,column=0,pady=5,columnspan=2)
		self.ger_label.grid(row=4,column=0,pady=(5,0),columnspan=2)
		self.ger_text.grid(row=5,column=0,pady=5,columnspan=2)
		self.eng_label.grid(row=6,column=0,pady=(5,0),columnspan=2)
		self.eng_text.grid(row=7,column=0,pady=5,columnspan=2)
		self.subButton.grid(row=8,column=1,pady=5,padx=5)
		self.clearButton.grid(row=8,column=0,pady=5,padx=5)
		self.quitButton.grid(row=0,column=0,pady=5,padx=5)
		self.backButton.grid(row=0,column=1,pady=5,padx=5)

	def submit(self):
		# find or create db
		# load df from db
		# append new input
		# clear inputs and focus ger_text
		if self.edit_state:
			self.tmp_db = self.entry.get()
		else:
			self.tmp_db = self.listvar.get()
		self.tmp_ger = self.ger_text.get("1.0",tk.END).rstrip()
		self.tmp_eng = self.eng_text.get("1.0",tk.END).rstrip()
		self.tmp_ger = self.tmp_ger.replace(",",";")
		self.tmp_eng = self.tmp_eng.replace(",",";")
		self.tmp_word = pd.DataFrame(
			[[self.tmp_ger,self.tmp_eng]],
			columns=['German','English'])
		self.append_it()
		self.clear_it()

	def append_it(self):
		self.lib = os.path.join("word_banks","{}.csv".format(self.tmp_db))
		try:
			self.df = pd.read_csv(self.lib)
		except FileNotFoundError:
			with open(self.lib,'w') as f:
				f.write("German,English\n")
			self.df = pd.read_csv(self.lib)
		self.df = pd.concat([self.df,self.tmp_word],
			axis=0,ignore_index=True)
		self.df.to_csv(self.lib,index=False)
		self.grab_csvs()

	def clear_it(self):
		self.ger_text.delete("1.0",tk.END)
		self.eng_text.delete("1.0",tk.END)
		self.ger_text.focus()

	def move_screens(self):
		self.frame.destroy()
		self.app = EditScreen1(self.master)

	def close_window(self):
		self.master.destroy()

def main():
	root = tk.Tk()
	root.title("Flash card database editor")
	app = EditScreen1(root)
	root.mainloop()

if __name__=="__main__":
	main()
