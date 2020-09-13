from game_matrix import game_matrix

def optimal(player_score, opponent_score):
    # take off the win_rate, not needed
    return game_matrix(player_score, opponent_score)[0]

def roll_4(player_score, opponent_score):
    return 4
