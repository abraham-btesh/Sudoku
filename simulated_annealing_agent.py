import random
import math
import numpy as np
from board import Board


class SA_Agent:

    def __init__(self, board: Board, temp, decay):
        self.board: Board = board
        self.board_size = board.get_board_size()
        if temp is not None:
            self.temp = temp
        else:
            self.temp = 10000
        if decay is not None and 0 < decay < 1:
            self.decay = decay
        else:
            self.decay = 0.99

        self.board.populate()
        self._initial = self.cost()
        self._final = None

    def cost(self):
        collisions = 0
        for value in range(1, self.board_size + 1, 1):
            collisions += self.count_row_collisions(self.board, value)
            collisions += self.count_column_collisions(self.board, value)
            collisions += self.count_sub_grid_collisions(self.board, value)
        return collisions


    def count_sub_grid_collisions(self, board, value):
        """
            counts the number of times a provided value appears in each subgrid. If it appears more than once, there is a
            collision and we return the count, the number of times it has been repeated.
            :param board: the board to check
            :param value: the value to check
            :return: the number of times a value has appeared more than once in the column, otherwise zero.
                """
        count = 0
        for i in range(0, self.board_size, int(math.sqrt(board.size))):
            for j in range(0, self.board_size, int(math.sqrt(board.size))):
                array = np.array(board.get_sub_grid_values(i, j))
                num_collisions = np.count_nonzero(array == value)
                if num_collisions > 1:
                    count += num_collisions
        return count

    def count_column_collisions(self, board, value):
        """
        counts the number of times a provided value appears in each column. If it appears more than once, there is a
        collision and we return the count, the number of times it has been repeated.
        :param board: the board to check
        :param value: the value to check
        :return: the number of times a value has appeared more than once in the column, otherwise zero.
        """
        count = 0
        for column in range(self.board_size):
            array = np.array(board.get_column(column))
            collision = np.count_nonzero(array == value)

            if collision > 1:
                count += collision

            return count

    def count_row_collisions(self, board, value):
        """
        counts the number of times a provided value appears in each row. If it appears more than once, there is a
        collision and we return the count, the number of times it has been repeated.
        :param board:
        :param value:
        :return:
        """
        count = 0
        for row in range(self.board_size):
            array = np.array(board.get_row(row))

            collision = np.count_nonzero(array == value)
            if collision > 1:
                count += collision

            return count

    def solve(self):
        T = self.temp
        decay = self.decay
        while T > 1:
            board = self.board
            coordinate1, coordinate2 = self.get_successors(board)
            if self.board.win():
                self._final = self.cost()
                return True
            current = self.cost()
            self.board.swap_coordinates(coordinate1, coordinate2)
            changed = self.cost()
            self.board.swap_coordinates(coordinate1, coordinate2)
            if current - changed > 0:
                self.board.swap_coordinates(coordinate1, coordinate2)
            else:
                penalty = current - changed
                if (math.exp(penalty/T) - random.uniform(0, 1)) > 0:
                    self.board.swap_coordinates(coordinate1, coordinate2)

            T *= decay

        self._final = self.cost()
        return False

    def get_successors(self, board):

        while True:
            row1 = random.randint(0, self.board_size)
            col1 = random.randint(0, self.board_size)
            row2 = random.randint(0, self.board_size)
            col2 = random.randint(0, board.size)
            if col1 != col2 and \
                    board.check_coordinates(row1, col1) and \
                    board.check_coordinates(row2, col2) and \
                    board.board[row1][col1] != board.board[row2][col2]:
                break
        return (row1, col1), (row2, col2)

    def get_difference(self):
        return self._initial - self._final
