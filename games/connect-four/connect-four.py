class ConnectFourSimulator:
	"""Creates a connect-4 board and simulates it, returning states and rewards for any taken action.

	The creates board is a 6 x 7 (rows x cols) array. Empty fields are denoted by 0.
	Tokens placed by player one are denoted by '1' and player two uses '-1'.
	Every field is part of the state and has it's own index, simply counting from 0 to 41 along the rows
	like so [
		[0, 1, 2, 3, 4, 5, 6],
		[7, 8, 9, 10, 11, 12, 13],
		...
		[35, 36, 37, 38, 39, 40, 41]
	]
	"""
	def __init__(self):
		self.width = 7
		self.height = 6
		self.board = np.zeros(shape=(self.height, self.width))
		self.PLAYER1 = 1
		self.PLAYER2 = -1
		self.DRAW = 0
		self.current_player = self.PLAYER1

	def take_action(self, action):
		"""Executes the action and returns the next state and the received reward."""
		inactive_player = self.__negated_player(self.current_player)
		if not self.__is_action_valid(action):
			return self.board, (self.current_player, -2), (inactive_player, 0)

		if self.__game_is_over():
			winner = self.__winner()
			if winner == self.DRAW:
				return self.board, (self.current_player, 0), (inactive_player, 0)
			elif winner == self.PLAYER1:
				return self.board, (self.current_player, 10), (inactive_player, 0)
			else:
				return self.board, (self.current_player, -10), (inactive_player, 0)

		self.__play_move(action)

		return self.board, (self.current_player, 0), (inactive_player, 0)

	def __play_move(self, action):
		"""Takes an action and executes it."""
		x, y = self.__coordinates_from_action(action)
		self.board[y][x] = self.current_player
		self.current_player = self.__negated_player(self.current_player)

	def __action_is_valid(self, action):
		"""Checks if the intended action is a valid one or if it breaks the rules of the game."""
		pass

	def __game_is_over(self):
		"""Returns True if the game is over and False otherwise."""
		pass

	def __winner(self):
		"""Returns the winner's number or 0 if the game resulted in a draw."""
		pass

	def __coordinates_from_action(self, action):
		"""Translates an action into (x, y) / (column, row) coordinates."""
		x = action % self.width
		y = action // self.width
		return x, y

	def __negated_player(self, player):
		"""Returns the player not passed to the function (Player1 if Player2 is passed and the other way around)."""
		return self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
