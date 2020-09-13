import random
import functools
from math import comb
import decimal

from rules import free_bacon, is_swine_align, is_pig_pass
from strategies import optimal, roll_4

def simulate(player_score, opponent_score, dice):
    if dice == 0:
        bacon = free_bacon(opponent_score)
        print(f"dice count of 0, {bacon=}")
        player_score += bacon
    else:
        rolls = random.choices(range(1, 7), k=dice)
        print(f"{rolls=}")
        if 1 in rolls:
            player_score += 1
        else:
            player_score += sum(rolls)
    return player_score

def take_turn(player, player_score, opponent_score):
    turn_over = False
    while not turn_over:
        turn_over = True

        dice = player(player_score, opponent_score)
        print(f"rolling {dice=}")
        player_score = simulate(player_score, opponent_score, dice)

        # bacon-align infinite combo is possible if
        # bacon = gcd(p, o), so swine-align triggers forever
        if player_score >= 100:
            turn_over = True
        elif is_swine_align(player_score, opponent_score):
            print("activated swine align")
            turn_over = False
        elif is_pig_pass(player_score, opponent_score):
            print("activated pig pass")
            turn_over = False
    return player_score, opponent_score

def check_game_over(score1, score2):
    assert(score1 < 100 or score2 < 100)

    if score1 >= 100:
        print("Player 1 won!\n")
        return 1

    if score2 >= 100:
        print("Player 2 won!\n")
        return -1

    return 0

def game(player1, player2):
    score1, score2 = 0, 0

    while True:
        print(f"player 1's turn, {score1} : {score2}")
        score1, score2 = take_turn(player1, score1, score2)
        if (result := check_game_over(score1, score2)) != 0:
            return result
        print(f"player 1's turn ends, {score1} : {score2}\n")

        print(f"player 2's turn, {score1} : {score2}")
        score2, score1 = take_turn(player2, score2, score1)
        if (result := check_game_over(score1, score2)) != 0:
            return result
        print(f"player 2's turn ends, {score1} : {score2}\n")

p1w = 0
for i in range(1000):
    result = game(optimal, roll_4)
    if result == 1:
        p1w += 1
print(p1w)
