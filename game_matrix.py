from functools import lru_cache
from math import comb
import decimal

from rules import free_bacon, is_swine_align, is_pig_pass

# assume standard dice
DICE_SIDE = 6

# maximum number of simultaneous rolls
MAX_ROLL = 10

# given some number of dice with specified sides/faces
# return number of possible rolls that sums to target
@lru_cache(maxsize=None)
def roll_chance(dice_side, dice_count, target):
    total = 0

    # formula from: http://mathforum.org/library/drmath/view/52207.html
    sum_top = (target - dice_count) // dice_side + 1
    for k in range(sum_top):
        total += ((-1) ** k
                * comb(dice_count, k)
                * comb(target - dice_side * k - 1,
                       dice_count - 1))

    return total

# calculate the chance of summing to target when case of rolling 1 is concern
def roll_chance_special_1(dice_side, dice_count, target):
    # using example of 6-sided dice
    # to calculate number of events where 1 is not rolled
    # but still sums to target
    # modify to 5 sided die with only sides 2-6
    # then transform 5-sided die with 2-6 to 5-sided die with 1-5
    total_events = decimal.Decimal(roll_chance(dice_side, dice_count, target))
    no_1 = decimal.Decimal(
        roll_chance(dice_side - 1, dice_count, target - dice_count))
    has_1 = total_events - no_1
    return (has_1, no_1)

# the win_rate at a particular cell
# when taken into account alternating turns
# and additional turn rules
@lru_cache(maxsize=None)
def win_rate(new_score, opponent_score):
    # win guaranteed with this score (already won)
    if new_score >= 100:
        return 1

    # if taking another turn, use the win_rate at that cell
    # equivalent to starting the turn there
    if (is_swine_align(new_score, opponent_score)
            or is_pig_pass(new_score, opponent_score)):
        return game_matrix(new_score, opponent_score)[1]

    # otherwise, opponent takes a turn,
    # win_rate is equivalent to opponent not winning in that situation
    return 1 - game_matrix(opponent_score, new_score)[1]

# construct the overall matrix lazily
# game_matrix(a, b), where a is score of current player
# and b is score of opponent, returns a tuple
# 1st: the optimal number of dice to roll for player a
# 2nd: the probability of player a winning if playing optimally
@lru_cache(maxsize=None)
def game_matrix(player_score, opponent_score):
    assert(player_score < 100 or opponent_score < 100)

    # choice does not matter, already won/lost
    if player_score >= 100:
        return (0, 1)
    elif opponent_score >= 100:
        return (0, 0)
    else:
        # assume 0 (free_bacon) is the best strategy
        best_dice_count = 0
        best_win_rate = win_rate(player_score + free_bacon(opponent_score),
                                 opponent_score)
        for dice_count in range(1, MAX_ROLL + 1):
            curr_win_rate = 0
            total_poss = DICE_SIDE ** dice_count

            for target in range(dice_count, dice_count * DICE_SIDE + 1):
                has_1, no_1 = roll_chance_special_1(
                    DICE_SIDE, dice_count, target)

                has_1_win_rate = (has_1
                                  * win_rate(player_score + 1, opponent_score)
                                  / total_poss)
                no_1_win_rate = (no_1
                                 * win_rate(player_score + target,
                                            opponent_score)
                                 / total_poss)

                curr_win_rate += has_1_win_rate + no_1_win_rate

            assert(curr_win_rate <= 1 and curr_win_rate >= 0)
            if curr_win_rate > best_win_rate:
                best_dice_count = dice_count
                best_win_rate = curr_win_rate

        return (best_dice_count, best_win_rate)

print(game_matrix(84, 99))
