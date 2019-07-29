"""
Advent of code, 2018
Day 8: Marble Mania
"""

# Performance-wise, the way to go is to use deque, rotate the circle and pop/append items

from typing import Tuple, NamedTuple
from collections import Counter, deque

# Circular buffer kind of thing

class Marbles():
    """
    class for the marbles game as defined in the problem statement
    """
    def __init__(self, num_players: int, total_num_marbles: int):
        """
        input: how many players, how many marbles to play
        """
        self.num_players = num_players
        self.total_num_marbles = total_num_marbles
        
        #self.marbles = [0]  # contains marble ids in their respective "slots" on the circle. First element 0 <=> Opening "move" played
        # Time complexities for Python lists
        # set O(1)
        # remove/delete O(n) 
        # --> this causes slowdown with large n 
        # --> USE deque and rotates with pop/append instead!
        
        self.marbles = deque([0])  # this is the circle
        self.player_in_turn = 1   # first player starts... player ids from 1 to num_players
        
        self.scores = Counter()   # store scores for each player. Player id as a key
    
        
    def play(self):
        """
        Plays the game of marbles until finish. Returns scores Counter
        """
        # 
        
        for marble_id in range(1, self.total_num_marbles + 1):
            if marble_id % 100000 == 0:
                print(marble_id)
            
            # the special case where marble number is multiple of 23
            if marble_id % 23 == 0:
                self.marbles.rotate(7)
                # the current player keeps the marble they would have placed, adding it to their score. 
                # Plus the marble seven steps to the left, which is removed
                self.scores[self.player_in_turn] += marble_id + self.marbles.pop()     # pops from the right end
                self.marbles.rotate(-1) 
            else:
                self.marbles.rotate(-1)  # move left by one, then the right end is the right place to append the new marble
                self.marbles.append(marble_id)   # append to the right end

            # player for the next round
            self.player_in_turn = self.player_in_turn + 1 if self.player_in_turn + 1 <= self.num_players else 1

        return self.scores


# unit tests:
"""10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""
assert Marbles(10, 1618).play().most_common(1)[0][1] == 8317
assert Marbles(13, 7999).play().most_common(1)[0][1] == 146373
assert Marbles(17, 1104).play().most_common(1)[0][1] == 2764
assert Marbles(21, 6111).play().most_common(1)[0][1] == 54718
assert Marbles(30, 5807).play().most_common(1)[0][1] == 37305


# Input:
# 455 players; last marble is worth 71223 points
with open("data/day09.txt") as f:
    input = f.read().split(";")

num_players = int(input[0].split(" ")[0])
num_marbles = int(input[1].split(" ")[-2])


game = Marbles(num_players, num_marbles)
scores = game.play()
#print(scores)
print("The resulting max score is", scores.most_common(1)[0][1])
# Right answer: 384288


###################3
# Part B:
# What would the new winning Elf's score be if the number of the last marble were 100 times larger?
new_game = Marbles(num_players, 100*num_marbles)
new_scores = new_game.play()  # slow with list-based implementation. Fast with deque + rotates
#print(new_scores)
print("The resulting max score is", new_scores.most_common(1)[0][1])
# Right answer: 3189426841
