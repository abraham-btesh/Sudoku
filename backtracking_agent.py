import random

from board import Board


class BacktrackingAgent:

    def __init__(self, board: Board, choosing_variable_heuristics=None, choosing_value_heuristics=None,
                 shuffle_variables=False, shuffle_values=False):
        self.board: Board = board
        self.board_size = board.get_board_size()
        self._shuffle_values = shuffle_values
        self._done_backtracking = 0

        if choosing_variable_heuristics is None:
            self.choosing_variable_heuristics = self.choose_variable_naively
        else:
            self.choosing_variable_heuristics = choosing_variable_heuristics
        if choosing_value_heuristics is None:
            self.choosing_value_heuristics = self.choose_value_naively
        else:
            self.choosing_value_heuristics = choosing_value_heuristics

        self.empty_coordinates_list = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board.get_assignment_at(row, col) == 0:
                    self.empty_coordinates_list.append((row, col))

        if shuffle_variables:
            random.shuffle(self.empty_coordinates_list)

    def solve(self):
        return self._backtracking(self.empty_coordinates_list.copy())

    def _backtracking(self, empty_coordinates_list):
        self._done_backtracking += 1
        if len(empty_coordinates_list) == 0:
            return True

        assignment = self.choosing_variable_heuristics(empty_coordinates_list)
        if assignment is None:
            return False
        row, col, legal_values = assignment
        empty_coordinates_list.remove((row, col))

        legal_values = self.choosing_value_heuristics(row, col, legal_values, empty_coordinates_list)

        for value in legal_values:
            previous_value = self.board.get_assignment_at(row, col)
            self.board.board[row, col] = value

            if self._backtracking(empty_coordinates_list.copy()):
                return True

            self.board.board[row, col] = previous_value

        return False

    def choose_variable_naively(self, empty_coordinates_list):
        row, col = empty_coordinates_list[0]
        legal_values = []

        for value in self.board.valid_values:
            if self.board.check_move_valid(value, row, col):
                legal_values.append(value)

        if len(legal_values) == 0:
            return None

        return row, col, legal_values

    def choose_value_naively(self, row, col, legal_values, empty_coordinates_list):
        if self._shuffle_values:
            random.shuffle(legal_values)

        return legal_values

    def get_done_backtracking(self):
        return self._done_backtracking
