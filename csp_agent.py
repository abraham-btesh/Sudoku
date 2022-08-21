from enum import Enum

from backtracking_agent import BacktrackingAgent
from board import Board


class CspHeuristic(Enum):
    MRV = 1
    LCV = 2


class CspAgent(BacktrackingAgent):

    def __init__(self, board: Board, choosing_variable_heuristics, choosing_value_heuristics, shuffle_variables=False,
                 shuffle_values=False):
        if choosing_variable_heuristics == CspHeuristic.MRV:
            choosing_variable_heuristics = self.minimum_remaining_values
        else:
            raise Exception('Unknown Heuristic!')

        if choosing_value_heuristics == CspHeuristic.LCV:
            choosing_value_heuristics = self.least_constrained_value
        else:
            raise Exception('Unknown Heuristic!')

        super().__init__(board, choosing_variable_heuristics, choosing_value_heuristics, shuffle_variables,
                         shuffle_values)

    def minimum_remaining_values(self, empty_coordinates_list):
        mrv = self.board_size
        assignment = None

        for row, col in empty_coordinates_list:
            legal_values = []
            for value in self.board.valid_values:
                if self.board.check_move_valid(value, row, col):
                    legal_values.append(value)

            if len(legal_values) == 0:
                return None
            if len(legal_values) <= mrv:
                mrv = len(legal_values)
                assignment = row, col, legal_values

        return assignment

    def least_constrained_value(self, row, col, legal_values, empty_coordinates_list):
        values_dict = dict()
        previous_value = self.board.get_assignment_at(row, col)

        for value in legal_values:
            loss = self._get_lcv_loss(row, col, value, previous_value, empty_coordinates_list)
            if loss is not None:
                values_dict[value] = loss

        return sorted(values_dict.keys(), key=lambda x: values_dict[x])

    def _get_lcv_loss(self, row, col, value, previous_value, empty_coordinates_list):
        loss = 0
        for r, c in empty_coordinates_list:
            values_counter_before_assignment = 0
            for v in self.board.valid_values:
                if self.board.check_move_valid(v, r, c):
                    values_counter_before_assignment += 1

            self.board.board[row, col] = value

            values_counter_after_assignment = 0
            for v in self.board.valid_values:
                if self.board.check_move_valid(v, r, c):
                    values_counter_after_assignment += 1

            self.board.board[row, col] = previous_value
            loss += values_counter_before_assignment - values_counter_after_assignment

            if values_counter_after_assignment == 0:
                return None

        return loss
