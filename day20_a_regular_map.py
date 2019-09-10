"""
Advent of code, 2018
Day 19: A Regular Map
Based on a reported shortcut (peculiarity of the data) that allows stack-based solution to work.
So this is not a general solution to the problem (different kind of input data would make it fail)
"""

from typing import Dict, Tuple, Union  # Union is "either"
import numpy as np

# distance dictionary type hint. For a coordinate, how many doors (minimum) one need to go thru to get there
DIST_DICT = Dict[Tuple[int], int]

# Inputs for unit tests:
RAW_TEST1 = "^WNE$"
RAW_TEST2 = "^ENWWW(NEEE|SSE(EE|N))$"
RAW_TEST3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
RAW_TEST4 = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
RAW_TEST5 = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"

# coordinate system. 
# East-West is the first "x" axis. East is +1
# South-North is the "y". South is +1
DIRECTIONS = {"N": (0,-1), "E": (1,0), "S": (0,1), "W":(-1,0)}

# Part One
# What is the largest number of doors you would be required to pass through to reach a room? 
# That is, find the room for which the shortest path from your starting location to that room would 
# require passing through the most doors; what is the fewest doors you can pass through to reach it?


def parse(regex:str, distances:DIST_DICT=None, x:int=0, y:int=0) -> Union[str, DIST_DICT]:
    # Do not fall into the mutable defaults trap
    # Expressions in default arguments are calculated when the function is defined, not when it’s called.
    # If the parse func had a default "=dict()" for the distances --> 
    # With each parse call we get reference to the same dict that may or may not be empty
    # So it can retain results from previous invocations 
    """returns the remaining regex string (internal, for recursion)
    and finally returns the distances Dictionary
    """
    if distances is None: distances = dict()

    # Recursive logic.
    # When facing branching, make recursive call to the parse func that will process the next option
    # It returns to the "parent" when we come to a new option, or branching closes
    # So that those options start at the parent, at correct position...
    # But, note, that this "stack-based" solution is quirk of the data reported e.g. on reddit
    # This shortcut makes this easier than the "true/complete" solution would have been. The thing is,
    # The logic does not generally track every possible route... When branch options have been explored, 
    # it continues from the previous pos before branching...Not from each of the branch end points (true path branching)

    while len(regex) > 0:
        instr = regex[0]  # the current character ("instruction") in the regex
        # if processing direction, update distances and position:
        if instr in DIRECTIONS:
            (dx, dy) = DIRECTIONS[instr]
            new_x, new_y = x+dx, y+dy

            # distance is either: 
            # a) "one plus the distance we came from" OR 
            # b) if the new position has been discovered earlier, its existing dist value if it is smaller
            distances[(new_x, new_y)] = min(distances[(x,y)]+1, distances.get((new_x, new_y), np.inf))
            x, y = new_x, new_y
        elif instr == "^":  # start
            distances[(x,y)] = 0
            # until the end of the regex, call recursively
            while instr != "$":
                regex = parse(regex[1:], distances, x, y)  # these modify the same distances dict
                instr = regex[0]
        # Handle those branches:
        elif instr == "(":
            while instr != ")":  # until the end of the branching instance
                regex = parse(regex[1:], distances, x, y)
                instr = regex[0]
        elif instr in ")$|":
            # "ends". Return to the calling function with the consumed regex string
            return regex
        regex = regex[1:]

    return distances


# Unit tests:
assert max(parse(RAW_TEST1).values()) == 3
assert max(parse(RAW_TEST2).values()) == 10
assert max(parse(RAW_TEST3).values()) == 18
assert max(parse(RAW_TEST4).values()) == 23
assert max(parse(RAW_TEST5).values()) == 31


# Read in the actual problem input
with open("data/day20.txt") as f:
    act_inp = f.read()

dists = parse(act_inp)

print("Solution to part 1:\nLargest number of doors required to pass through to reach a (most distant) room? Answer:")
print(max(dists.values()))  # Correct answer: 3991


# PART TWO
# How many rooms have a shortest path from your current location that pass through at least 1000 doors?
print("\nSolution to part 2:")
print("How many rooms have a shortest path from your current location that pass through at least 1000 doors? Answer:")
print(sum(dist >= 1000 for dist in dists.values()))  # 8394