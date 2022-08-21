import random
from typing import List
import math
from board import Board


class SBS_Agent:

    def __init__(self, board: Board, iterations):
        self.board = board
        self.stochasticSize = 10
        if iterations is not None:
            self.counter = iterations
        else:
            self.counter = 100000
        self.board_list: List[Board] = self.build_boards(board, self.stochasticSize)
        self.board_size = board.get_board_size()
        board.populate()

    def build_boards(self, board: Board, amount) -> List[Board]:
        lst = []
        for amt in range(amount):
            b1 = Board(board.entries, board.size)
            b1.populate()
            lst.append(b1)
        return lst

    def cost(self, board):
        collisions = 0
        collisions += self.count_row_collisions(board)
        collisions += self.count_column_collisions(board)
        collisions += self.count_sub_grid_collisions(board)

        return collisions



    def count_sub_grid_collisions(self, board):
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
                s = set()
                if board.board[i][j] in s:
                    count += 1
                s.add(board.board[i][j])

        return count


    def count_column_collisions(self, board):
        """
        counts the number of times a provided value appears in each column. If it appears more than once, there is a
        collision and we return the count, the number of times it has been repeated.
        :param board: the board to check
        :param value: the value to check
        :return: the number of times a value has appeared more than once in the column, otherwise zero.
        """
        count = 0
        for c in range(self.board_size):
            s = set()
            col = board.get_column(c)
            for i in col:
                if i in s:
                    count += 1
                s.add(i)


        return count


    def count_row_collisions(self, board):
        """
        counts the number of times a provided value appears in each row. If it appears more than once, there is a
        collision and we return the count, the number of times it has been repeated.
        :param board:
        :param value:
        :return:
        """
        count = 0
        for r in range(self.board_size):
            s = set()
            row = board.get_row(r)
            for i in row:
                if i in s:
                    count += 1
                s.add(i)


        return count


    def solve(self):
        for _ in range(self.counter):
            for index, board in enumerate(self.board_list):
                beamLst = []
                for _ in self.board_list:
                    while True:
                        row1 = random.randint(0, board.size)
                        col1 = random.randint(0, board.size)
                        row2 = row1
                        col2 = random.randint(0, board.size)
                        if col1 != col2 and \
                            board.check_coordinates(row1, col1) and \
                                board.check_coordinates(row2, col2) and\
                                board.board[row1][col1] != board.board[row2][col2]:
                            beamLst.append([(row1, col1), (row2, col2)])
                            break
                    if board.win():
                        self.board.board = board.board
                        return True
                if random.uniform(0, 1) > 0.8:
                    pick = beamLst[random.randint(0, len(beamLst) - 1)]
                    boardCost = self.cost(board)
                    board.swap_coordinates(pick[0], pick[1])
                    newCost = self.cost(board)
                    board.swap_coordinates(pick[0], pick[1])

                    if newCost < boardCost:
                        board.swap_coordinates(pick[0], pick[1])
                    else:
                        if random.uniform(0, 1) > 0.8:
                            new_board = Board(board.entries, board.size)
                            new_board.populate()
                            self.board_list[index] = new_board
                else:
                    best_b = beamLst[0]
                    board.swap_coordinates(best_b[0], best_b[1])
                    penalty = self.cost(board)
                    board.swap_coordinates(best_b[0], best_b[1])
                    for b in beamLst:
                        board.swap_coordinates(b[0], b[1])
                        p1 = self.cost(board)
                        board.swap_coordinates(b[0], b[1])
                        if p1 < penalty:
                            penalty = p1
                            best_b = b
                    myCost = self.cost(board)
                    if penalty < myCost or random.uniform(0, 1) > 0.8:
                        board.swap_coordinates(best_b[0], best_b[1])

        for board in self.board_list:
            if self.cost(board) < self.cost(self.board):
                self.board.board = board.board

        if self.board.win():
            return True

        return False
