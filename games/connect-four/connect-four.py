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
		self.valid_actions = list(range(self.width))
		self.__game_over = False

	def take_action(self, action):
		"""Executes the action and returns the next state and the received reward."""
		assert not self.__game_over, "Game is already finished."

		if not self.__action_is_valid(action):
			return self.__game_over, self.board, (-2, 0)

		x, y = self.__coordinates_from_action(action)
		self.__play_move(x, y)

		self.__game_over = self.__game_is_over(x, y)
		if self.__game_over:
			winner = self.__winner(x, y)
			if winner == self.DRAW:
				return self.__game_over, self.board, (0, 0)
			return self.__game_over, self.board, (1, -1)

		return self.__game_over, self.board, (0, 0)

	def print_board(self):
		board = self.board
		board = np.where(board == 1, "X", board)
		board = np.where(board == "-1.0", "O", board)
		print(np.where(board == "0.0", "-", board))

	def __play_move(self, x, y):
		"""Takes an action and executes it."""
		self.board[y][x] = self.current_player
		self.current_player = self.__negated_player(self.current_player)

	def __action_is_valid(self, action):
		"""Checks if the intended action is a valid one or if it breaks the rules of the game."""
		is_valid = action in self.valid_actions

		if is_valid:
			if self.__column_height(action) >= (self.height - 1):
				self.valid_actions.remove(action)
		return is_valid

	def __column_height(self, x):
		"""Returns the height of a column which is equal to the amount of tokens placed."""
		column = self.board[:, x]
		return np.count_nonzero(column)

	def __game_is_over(self, x, y):
		"""Returns True if the game is over and False otherwise."""
		if np.count_nonzero(self.board) >= 42:
			return True

		lines = self.__extract_lines(x, y)

		for line in lines:
			if self.__winner_in_line(line) != 0:
				return True

		return False

	def __extract_lines(self, x, y):
		"""Extracts the horizontal, vertical and the diagonal lines going through the last action"""
		row = self.board[y]
		column = self.board[:, x]
		top_down_diagonal = self.board.diagonal(x - y)

		mirrored_x = self.width - 1 - x
		bot_up_diagonal = np.fliplr(self.board).diagonal(mirrored_x - y)

		return row, column, top_down_diagonal, bot_up_diagonal

	def __winner(self, x, y):
		"""Returns the winner's number or 0 if the game resulted in a draw (Requires the game to have ended)."""
		lines = self.__extract_lines(x, y)

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
		return action, self.__column_height(action)

	def __negated_player(self, player):
		"""Returns the player not passed to the function (Player1 if Player2 is passed and the other way around)."""
		return self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
