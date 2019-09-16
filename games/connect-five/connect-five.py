import numpy as np

class ConnectFive:
	def __init__(self, sizeX, sizeY):
		self.__board = np.zeros((sizeX, sizeY))
		self.__current_player = 1

	def move(self, x, y):
		'''
			Play a move and return True if the game is finished.

			Args:
				x: The x coordinate of the move
				y: The y coordinate of the move

			Returns:
				False if the game is not yet over after the move
				True if the game is over after the move

			Raises:
				WrongMoveError: If the move has already been played or is out of the board's size
		'''
		if x < 0 or x >= self.__board.shape[0]:
			raise WrongMoveError("x value is out of board size")
		if y < 0 or y >= self.__board.shape[1]:
			raise WrongMoveError("y value is out of board size")
		if self.__board[x][y] != 0:
			raise WrongMoveError("This move has already been played")

		if self.__winner(self.__board, x, y) == 0:
			self.__current_player = (self.__current_player % 2) + 1
			return False
		return True

	def __winner(self, board, x, y):
		'''
			Returns the winner of the current game.

			Returns:
				0 if the game is not yet over
				1 if player one has won the game
				2 if player two has won the game
		'''
		row = board[x]
		winner = self._check_list_for_win(row)
		if winner != 0:
			return winner

		column = board[:, y]
		winner = self._check_list_for_win(column)
		if winner != 0:
			return winner

		diagonal_to_bot = board.diagonal(y - x)
		winner = self._check_list_for_win(diagonal_to_bot)
		if winner != 0:
			return winner

		diagonal_to_top = np.fliplr(board).diagonal(board.shape[1] - 1 - abs(y - x))
		winner = self._check_list_for_win(diagonal_to_top)
		if winner != 0:
			return winner

		return 0

	def __check_list_for_win(self, list):
		sum = 0
		for field in list:
			if field == self.__current_player:
				sum += 1
			else:
				sum = 0
			if sum == 5:
				return self.__current_player
		return 0


	class Error(Exception):
		'''Base class for exceptions in this module.'''
		pass

	class WrongMoveError(Error):
		'''Exception raised if the attempted move is invalid.

			A move is invalid if it played outside of the field or in a
			position that has already been played
		'''

		def __init__(self, message):
			self.message = message
