pi = '3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196'

def gcd(a, b):
    assert(a != 0 and b != 0)
    while b != 0:
        a, b = b, a % b
    return a

def free_bacon(opponent_score):
    k = 0
    if opponent_score == 0:
        k = 3
    else:
        assert(opponent_score < 200)
        k = int(pi[opponent_score + 2])
    return k + 3

def is_swine_align(player_score, opponent_score):
    return player_score > 0 and opponent_score > 0 and gcd(player_score, opponent_score) >= 10

def is_pig_pass(player_score, opponent_score):
    return player_score < opponent_score and opponent_score - player_score < 3
