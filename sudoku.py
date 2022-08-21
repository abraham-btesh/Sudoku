import argparse
from datetime import datetime

from simulated_annealing_agent import SA_Agent
from stochastic_beam_search import SBS_Agent
import file_parser
from backtracking_agent import BacktrackingAgent
from board import Board
from csp_agent import CspAgent, CspHeuristic


class GameRunner:
    def __init__(self, agent, board):
        self.agent = agent
        self.board = board

    def run(self):
        start = datetime.now()
        if self.agent.solve():
            assert self.board.win()
            print(self.board)
        else:
            assert not self.board.win()
            print('agent could not solve this board!')

        print(f'running time: {datetime.now() - start}')

        if isinstance(self.agent, BacktrackingAgent):
            print(f'number of backtracking calls: {self.agent.get_done_backtracking()}')
            print('*******************************************\n')
            return self.agent.get_done_backtracking()
        elif isinstance(self.agent, SA_Agent):
            print(f'improvement: {self.agent.get_difference()}')
            print('*******************************************\n')
            return self.agent.get_difference()

        print('*******************************************\n')
        return 0



def create_agent(args, board):
    if args.agent == 'BacktrackingAgent':
        print('Agent: Backtracking Agent')
        return BacktrackingAgent(board, None, None)
    elif args.agent == 'CspAgent':
        print('Agent: Csp Agent')
        return CspAgent(board, CspHeuristic.MRV, CspHeuristic.LCV)
    elif args.agent == 'SA_Agent':
        print("Simulated Annealing Agent")
        return SA_Agent(board, args.temp, args.decay)
    elif args.agent == 'SBS_Agent':
        print("Stochastic Beam Agent")
        return SBS_Agent(board, args.iterations)


def main(args):
    start = datetime.now()
    print(f'\n\nsolving boards in file: {args.games_file}..')

    games = file_parser.read_games(args.games_file)

    if args.number_of_boards is not None:
        number_of_boards = int(args.number_of_boards)
        assert 0 <= number_of_boards <= len(games), 'number of boards is not valid!'
        games = games[:number_of_boards]

    change = 0
    for idx, entries in enumerate(games):
        print(f'solving board num. {idx + 1}')
        board = Board(entries, args.board_size)
        agent = create_agent(args, board)
        game_runner = GameRunner(agent, board)
        change += game_runner.run()

    duration = datetime.now() - start
    average_running_time = duration / len(games)
    print("end time: " + str(duration))
    print(f"average running time: {average_running_time} (in seconds: {average_running_time.total_seconds()})")

    average_change = change / len(games)
    if args.agent in {'BacktrackingAgent', 'CspAgent'}:
        print(f"average of backtracking calls: {average_change}")
    elif args.agent == 'SA_Agent':
        print(f"average improvement: {average_change}")

    return average_running_time.total_seconds(), average_change


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='Sudoku game.')
    args_parser.add_argument('--games_file', help='file of Sudoku boards.', type=str)
    args_parser.add_argument('--board_size', help='The board size.', type=int)
    args_parser.add_argument('--number_of_boards', help='number of boards to be solved in games_file, '
                                                        'if you want to solve all boards in games_file, '
                                                        'please, do not fill this parameter!', default=None)
    agents = ['BacktrackingAgent', 'CspAgent', 'SA_Agent', 'SBS_Agent']
    args_parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[1], type=str)
    args_parser.add_argument('--temp', help='The highest temperature', type=int)
    args_parser.add_argument('--decay', help='The rate of decay.', type=float)
    args_parser.add_argument('--iterations', help='The number of iterations', type=int)



    _args = args_parser.parse_args()
    main(_args)
