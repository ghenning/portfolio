class Board:

	# the tic-tac-toe game board, creates the board, handles winning
	# conditions, resets the game if asked 

	def __init__(self):
		""" initialize the game, this way it can be restarted easily """
		self.initialize_game()

	def initialize_game(self):
		""" set up all the necessary things """
		self.generate_board()
		self.print_instructions()
		self.player = 'X'
		self.winner = None
		self.turn = 1
		self.game_on = 1
		self.print_board()
		self.play_game()

	def generate_board(self):
		""" create a 3x3 board """
		self.board = [['-' for i in range(3)] for j in range(3)]

	def print_board(self):
		""" print the game board in its current state """
		breaks = ['\n','\n','']
		print('\n')
		[print("{}{}".format(" ".join(line),sep)) for line,sep in zip(self.board,breaks)]
		print('\n')

	def place_piece(self):
		""" placing a game piece (X or O) """
		# whose turn is it?
		print("it's {}'s turn".format(self.player))
		move = input("Place your {}\t".format(self.player)).strip()
		# input 'q' to end the game
		if move.lower() == 'q':
			self.game_on = 0
			return
		# assume people may input coordinates in different ways
		move = move.replace(' ','').replace(',','').replace('.','')
		loc = [xy for xy in move]
		# weird user input handling
		if len(loc) < 2:
			loc = ['',''] # in case less than 2 digits are given
		# if the input makes sense, continue. else, try again
		if (loc[0] in ['1','2','3']) and (loc[1] in ['1','2','3']):
			x = int(loc[1])-1
			y = int(loc[0])-1
			# check if tile is empty. else, try again
			if self.board[y][x] == '-':
				self.board[y][x] = self.player
				self.print_board()
				self.turn += 1
				# if winning condition is met, end the game loop
				if self.check_endgame():
					self.game_on = 0	
				else:
					self.swap_player()
			else:
				print("game piece already there, try again")
		else:
			print('invalid move, try again')

	def check_endgame(self):
		""" check winning conditions, columns/rows/diagonals """
		#checking columns
		for i in range(3):
			tmp_col = [self.board[k][i] for k in range(3)]
			if tmp_col == [self.player]*3:
				self.winner = self.player
				return 1

		#checking rows
		for i in range(3):
			tmp_col = [self.board[i][k] for k in range(3)]
			if tmp_col == [self.player]*3:
				self.winner = self.player
				return 1

		#checking diagonals
		tmp_col = [self.board[i][i] for i in range(3)]
		if tmp_col == [self.player]*3:
			self.winner = self.player
			return 1

		tmp_col = [self.board[2-i][i] for i in range(3)]
		if tmp_col == [self.player]*3:
			self.winner = self.player
			return 1

	def swap_player(self):
		""" swap between players X/O """
		if self.player == 'X':
			self.player = 'O'
		else:
			self.player = 'X'

	def print_instructions(self):
		""" print instructions """
		print("\n\n")
		print("You're playing tic-tac-toe, everyone knows the rules")
		print("Place your Xs and Os by inputting coordinates")
		print("E.g. 12 will put a piece in the first line, second column")
		print("Input q to quit\n")

	def play_game(self):
		""" the game loop. ends when one player wins or board is filled """
		while self.game_on and self.turn < 10:
			self.place_piece()
		self.end_game()

	def end_game(self):
		""" end game message """
		print("\nGame Over\n")
		if self.winner:
			print("{} wins!".format(self.player))
		else:
			print("Draw!")

		self.play_again()

	def play_again(self):
		""" restart the game loop if the players want to """
		again = input("\nPlay again? (Y/N)\t").lower()
		if again == 'y':
			self.initialize_game()
