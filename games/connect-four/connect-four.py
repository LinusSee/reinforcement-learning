import numpy as np

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
		self.__game_over = False

	def take_action(self, action):
		"""Executes the action and returns the next state and the received reward."""
		inactive_player = self.__negated_player(self.current_player)
		if not self.__action_is_valid(action):
			return self.__game_over, self.board, (self.current_player, -2), (inactive_player, 0)

		self.__play_move(action)

		self.__game_over = self.__game_is_over(action)
		if self.__game_over:
			winner = self.__winner(action)
			if winner == self.DRAW:
				return self.__game_over, self.board, (self.current_player, 0), (inactive_player, 0)
			elif winner == self.PLAYER1:
				return self.__game_over, self.board, (self.current_player, 10), (inactive_player, -10)
			else:
				return self.__game_over, self.board, (self.current_player, -10), (inactive_player, 10)

		return self.__game_over, self.board, (self.current_player, 0), (inactive_player, 0)

	def print_board(self):
		print(self.board)

	def __play_move(self, action):
		"""Takes an action and executes it."""
		x, y = self.__coordinates_from_action(action)
		self.board[y][x] = self.current_player
		self.current_player = self.__negated_player(self.current_player)

	def __action_is_valid(self, action):
		"""Checks if the intended action is a valid one or if it breaks the rules of the game."""
		if action < 0:
			return False
		x, y = self.__coordinates_from_action(action)
		if x >= self.width or y >= self.height:
			return False

		height_x = self.__column_height(x)

		if y < height_x:
			return False
		return True

	def __column_height(self, x):
		"""Returns the height of a column which is equal to the amount of tokens placed."""
		column = self.board[:, x]
		return np.count_nonzero(column)

	def __game_is_over(self, last_action):
		"""Returns True if the game is over and False otherwise."""
		if np.count_nonzero(self.board) == 0:
			return True

		lines = self.__extract_lines(last_action)

		for line in lines:
			if self.__winner_in_line(line) != 0:
				return True

		return False

	def __extract_lines(self, last_action):
		"""Extracts the horizontal, vertical and the diagonal lines going through the last action"""
		x, y = self.__coordinates_from_action(last_action)

		row = self.board[y]
		column = self.board[:, x]
		top_down_diagonal = self.board.diagonal(x - y)

		mirrored_x = self.width - 1 - x
		bot_up_diagonal = np.fliplr(self.board).diagonal(mirrored_x - y)

		return row, column, top_down_diagonal, bot_up_diagonal

	def __winner(self, last_action):
		"""Returns the winner's number or 0 if the game resulted in a draw (Requires the game to have ended)."""
		lines = self.__extract_lines(last_action)

		for line in lines:
			winner = self.__winner_in_line(line)
			if winner != 0:
				return winner

		return 0

	def __winner_in_line(self, line):
		"""Checks if a line contains a winner and returns his number if yes and 0 otherwise."""
		token_sum = 0
		for token in line:
			token_sum += token
			if token_sum == 4 * self.PLAYER1:
				return self.PLAYER1
			if token_sum == 4 * self.PLAYER2:
				return self.PLAYER2
			if token_sum < 0 < token or token_sum > 0 > token:
				token_sum = 0
		return 0

	def __coordinates_from_action(self, action):
		"""Translates an action into (x, y) / (column, row) coordinates."""
		x = action % self.width
		y = action // self.width
		return x, y

	def __negated_player(self, player):
		"""Returns the player not passed to the function (Player1 if Player2 is passed and the other way around)."""
		return self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
