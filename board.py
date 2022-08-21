import numpy as np
import math
import random


class Board:

    def __init__(self, entries, size):
        """
        a constructor for a Sudoku board. It takes an array of the starting state of the board and
        builds a numpy array
        :param entries: a list of numbers, which are in string form, which represent the starting
        position of the Sudoku board
        :param size: the dimensions of the board will be size*size
        """
        self.size = size
        self.entries = entries
        self.valid_values = [val + 1 for val in range(size)]  # a list of the values which can be added
        self.unchangeable_coordinates = []  # a list of tuples which will hold the coordinates which can not be changed
        self.board = np.zeros((self.size, self.size))
        self.build_board_from_entries(entries)
        self.initialize_unchangeable_coordinates()

    def build_board_from_entries(self, entries):
        """
        Builds a board/numpy array from a list of strings, which must be convertible into integers.
        An empty spot on the sudoku board is represented by  a zero. The strings must represent numbers
        between 1 and the size of the board. Otherwise this will result in errors
        :param entries: a list of string representations of numbers
        :return: a numpy array as a sudoku board which can now be played on.
        """

        self.board = np.array([int(character) for character in entries]).reshape(self.size, self.size)

    def initialize_unchangeable_coordinates(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row, column] != 0:
                    self.unchangeable_coordinates.append((row, column))

    def place(self, num, row, column):
        """
        places the provided number in the x,y position on the board
        :param num: the number to be placed. It must be within the acceptable limits of the board
        :param row: the row coordinate
        :param column: the column coordinate
        :return: nothing
        """
        if not self.check_move_valid(num, row, column):
            raise Exception("the input is outside the acceptable ranges. ")
        self.board[row, column] = num

    def check_move_valid(self, num, row, column):
        """
        checks if placing the number provided in the coordinates provided is a valid move
        :param num: the number to place
        :param row: the row coordinate
        :param column: the column coordinate
        :return: True if the move is valid otherwise false
        """

        # the number is not in the acceptable range
        if num not in self.valid_values:
            return False

        # the coordinates are valid
        if not self.check_coordinates(row, column):
            return False

        row_values = self.get_row(row)
        column_values = self.get_column(column)

        # the number already exists in the row or column
        if num in row_values or num in column_values:
            return False

        # the value is not in the sub grids
        if not self.check_val_in_sub_grids(num, row, column):
            return False

        return True

    def check_coordinates(self, row, column):
        """
        checks if the coordinates are valid, whether the row and column inputs are within acceptable ranges and
        whether the coordinates
        :param row: the row to check
        :param column: the column to check
        :return: True if the coordinates are valid otherwise False
        """

        # the provided coordinates are unchangeable
        if (row, column) in self.unchangeable_coordinates:
            return False

        # the coordinates are acceptable
        if (not 0 <= row < self.size) or (not 0 <= column < self.size):
            return False

        return True

    def check_val_in_sub_grids(self, value, row, column):
        """
        checks if the value is in the sub_grid which (row, column) is in
        :param value: the value we want to place
        :param row: the row coordinate
        :param column: the column coordinate
        :return: False if the value is already in the sub grid and cant be placed, True otherwise
        """
        grid_row, grid_column = self.get_sub_grid_coordinates(row, column)
        sub_grid = self.get_sub_grid_values(grid_row, grid_column)
        if value in sub_grid:
            return False

        return True

    def get_sub_grid_coordinates(self, row, column):
        """
        find the upper left corner of the subgrid in which the coordinates (row, column) are
        :param row:
        :param column:
        :return: a tuple of the coordinates the sub_grid in which the coordinates belong
        """
        grid_row = 0
        grid_column = 0

        for i in range(0, self.size, int(math.sqrt(self.size))):
            if i <= row < i + int(math.sqrt(self.size)):
                grid_row = i

        for j in range(0, self.size, int(math.sqrt(self.size))):
            if j <= column < j + int(math.sqrt(self.size)):
                grid_column = j

        return grid_row, grid_column

    def get_row(self, row):
        """
        returns the row described by the input from the current board as an array
        :param row: the row we want to look at
        :return: an array of the values in the described row
        """
        return self.board[row]

    def get_column(self, column):
        """
        returns the column number described as an array so that it can be analyzed
        :param column: the column number we want to look at
        :return: an array of the values in the described column
        """
        return self.board[:, column]

    def win(self):
        """
        checks to see if a board has been completed.
        :return: True if the board has been successfully completed False otherwise
        """

        # check if all the rows contain all the numbers
        return self.check_rows_and_columns() and self.check_sub_grids()


    def check_rows_and_columns(self):
        """
        checks that the rows and columns contain all the values they should in order for
        a sudoku board to be completed.
        :return: True if each row contains all the values 1,..., self.size and each column contains
        all the values 1,...,self.size. Otherwise the function will return false
        """
        for i in range(self.size):
            row_values = self.get_row(i)  # row #i
            column_values = self.get_column(i)  # column #i
            for j in range(1, self.size + 1, 1):
                # the row or the column does not contain one of the required values
                if j not in row_values or j not in column_values:
                    return False

        return True


    def check_sub_grids(self):
        """
        checks that all the sub-grids contain the the required value
        :return: True if all the values 1,..., self.size are in each grid and False otherwise
        """
        for i in range(0, self.size, int(math.sqrt(self.size))):
            for j in range(0, self.size, int(math.sqrt(self.size))):
                # check the grid whose upper left corner is in the coordinate (i,j)
                values = self.get_sub_grid_values(i, j)

                for s in range(1, self.size + 1, 1):
                    if s not in values:
                        return False

        return True

    def get_sub_grid_values(self, row, column):
        """
        gets the values in the grid whose upper left corner is row,column
        :param row: the row of the upper left corner
        :param column: the column
        :return: a list of values in the grid
        """
        values = []
        for i in range(int(math.sqrt(self.size))):
            for j in range(int(math.sqrt(self.size))):
                values.append(self.board[row + i, column + j])

        return values

    def get_copy_of_board(self):
        return self.board.copy()

    def get_board_size(self):
        return self.size

    def get_assignment_at(self, row, col):
        return self.board[row, col]

    def swap_coordinates(self, coordinate1, coordinate2):
        """
        swaps the values held in the board at coordinate1 and coordinate2
        :param coordinate1: a tuple of the form (row, column)
        :param coordinate2: a tuple of the form (row, column)
        :return:
        """

        if not self.check_coordinates(coordinate1[0], coordinate1[1]) or not self.check_coordinates(coordinate2[0],
                                                                                                    coordinate2[1]):
            raise Exception("There has been an error. These are not changeable coordinates")

        val1 = self.board[coordinate1[0]][coordinate1[1]]
        val2 = self.board[coordinate2[0], coordinate2[1]]

        self.board[coordinate1[0], coordinate1[1]] = val2
        self.board[coordinate2[0], coordinate2[1]] = val1

    def populate(self):
        """
        populates the board with all the values required to successfully solve the sudoku board. IE all the missing
        pieces are now on the board. They just need to be moved into place.
        :return:
        """
        for row in range(self.size):
            s = set(list(range(1, self.size + 1)))
            for i in self.board[row]:
                if i == 0:
                    continue
                s.remove(i)
            for i in range(self.size):
                if self.board[row][i] == 0:
                    rand_choice = random.choice(tuple(s))
                    s.remove(rand_choice)
                    self.board[row][i] = rand_choice



    def is_fixed_coordinate(self, row, col):
        return (row, col) in self.unchangeable_coordinates


    def __str__(self):
        """
        :return: returns a string representation of the board
        """
        size_sqrt = int(math.sqrt(self.size))
        line_num = (size_sqrt + self.size + 1) * 2
        line = ' ' + '-' * line_num + '\n'

        string = ''
        for row in range(self.size):
            if row % size_sqrt == 0:
                string += line

            to_print = ''
            for col in range(self.size):
                if col % size_sqrt == 0:
                    to_print += ' |'
                to_print += ' ' + str(self.board[row, col])

            string += to_print + ' |\n'

        string += line
        return string
