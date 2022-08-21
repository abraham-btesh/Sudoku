

def read_games(games_file):
    f = open(games_file, "r")
    game_string = f.read()

    games = game_string.split("\n\n")

    # final games holds a list of list where each list is a separate string representation of the game
    final_games = [[character.strip() for line in games[i].split("\n") for character in line.split()]
                   for i in range(len(games))]

    return final_games
