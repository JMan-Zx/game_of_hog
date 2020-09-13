# The Game of Hog
A short implementation of The Game of Hog.

Details about the game can be found at https://cs61a.org/proj/hog/#phase-1-simulator

## Rules
The variant implemented here contains the following rules.

### Basics
Players alternate turns to try to end their turn with 100 points (or more).
Each turn, the active player may choose to roll 1 - 10 dice.
The sum of the dice rolls is added to their points

### Pig Out. 
If any of the dice outcomes is a 1, the current player's score for the turn is 1.

### Free Bacon. 
A player who chooses to roll zero dice scores k+3 points, where k is the nth digit of pi after the decimal point, and n is the total score of their opponent. As a special case, if the opponent's score is n = 0, then k = 3 (the digit of pi before the decimal point).

### Swine Align. 
After points for the turn are added to the current player's score, if both players have a positive score and the Greatest Common Divisor (GCD) of the current player's score and the opponent's score is at least 10, take another turn.

### Pig Pass. 
After points for the turn are added to the current player's score, if the current player's score is lower than the opponent's score and the difference between them is less than 3, the current player takes another turn.

## Strategies
A strategy that should be optimal for the specified variant is provided.

### Optimal
A game matrix is calculated and cached in which every choice made (the number of dice to roll) theoretically maximizes chance of winning.
Note that this is different from maximizing score.

### Computation Time
Due to implementation inefficiencies, the initial computation of the matrix may take ~1s.
This can be optimized in various ways: storing various probabilities of dice rolls before hand, replacing lru_cache hack with proper memoization,
or just storing the entire optimal dice roll matrix (which should take no more than 20k characters).
