"""
Advent of code, 2018
Day 18: Settlers of The North Pole
"""

from typing import Dict, Tuple
from collections import Counter, defaultdict

Pos = Tuple[int, int]
Grid = Dict[Pos, str]

# given test case
RAW = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

def parse_initial_state(string:str) -> Grid:
    lines = string.splitlines()
    grid = {(x,y): char for y, line in enumerate(lines) for x, char in enumerate(line)}

    return grid


def show(grid:Grid, do_print=True) -> None:
    x_lo = min(x for x, y in grid.keys())
    x_hi = max(x for x, y in grid.keys())
    y_lo = min(y for x, y in grid.keys())
    y_hi = max(y for x, y in grid.keys())

    rows = [[grid.get((x, y)) 
            for x in range(x_lo, x_hi + 1)]
            for y in range(y_lo, y_hi + 1)]

    string = "\n".join(''.join(row) for rowno, row in enumerate(rows))
    if do_print:
        print(string)
    
    return string


def get_adjacent_counts(grid: Grid, pos: Pos) -> Dict[str, int]:  # outputs a Counter
    xp, yp = pos
    adj_counts = Counter([grid.get((x,y)) 
                            for x in range(xp-1, xp+2) 
                            for y in range(yp-1, yp+2) 
                            if (x,y) != (xp,yp)])  # except x,y itself

    return adj_counts


def get_resource_value(grid: Grid) -> int:
    num_wooden = sum(1 for content in grid.values() if content == "|")
    num_lumberyard = sum(1 for content in grid.values() if content == "#")

    return num_wooden * num_lumberyard


def step(grid: Grid, num_minutes: int = 1, show_grid=True) -> Grid:
    for rnd in range(num_minutes):
        new_grid = grid.copy()

        for pos, content in grid.items():
            adj_counts = get_adjacent_counts(grid, pos)
            # An open acre will become filled with trees if three or more adjacent acres contained trees
            # Otherwise, nothing happens.
            if content == ".":
                if adj_counts["|"] >= 3:
                    new_grid[pos] = "|"

            # An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. 
            # Otherwise, nothing happens.
            elif content == "|":
                if adj_counts["#"] >= 3:
                    new_grid[pos] = "#"

            # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard 
            # and at least one acre containing trees. Otherwise, it becomes open.
            elif content == "#":
                if not (adj_counts["#"] >= 1 and adj_counts["|"] >= 1):
                    new_grid[pos] = "."

        grid = new_grid  # apply all changes at the same time

        if show_grid:
            print(f"\nround {rnd}: ")
            show(grid)

    return grid


# Test case with unit tests
test_grid = parse_initial_state(RAW)

test_grid = step(test_grid, 10)
assert show(test_grid) == """.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||"""

assert get_resource_value(test_grid) == 1147


# Read in actual problem input:
with open("data/day18.txt") as f:
    grid_init = parse_initial_state(f.read())

grid = step(grid_init, 10)
print("Total res. value after 10 rounds: ", get_resource_value(grid))
# 384416 was the right answer


###############
# PART TWO:
# What will the total resource value of the lumber collection area be after 1_000_000_000 minutes?
# Would take infeasibly long. There probably is a repeating state -> starts to cycle -> can skip ahead.

# the process is deterministic. If we see some state again, we know we will be cycling between the start and end state indefinitely

FIND_CYCLE = False

if FIND_CYCLE:
    seen = set()
    seen_dict = defaultdict(list) # str representation of the state as key, iteration# as values

    grid = grid_init
    for i in range(10000):
        grid = step(grid, 1, show_grid=False)
        print(f"Total res. value after {i+1} rounds: ", get_resource_value(grid))
        grid_str = show(grid, do_print=False)
        seen_dict[grid_str].append(i)
        if grid_str in seen:
            print("seen the following setup before:")
            print(show(grid))
            print("\nseen_dict:")
            print(seen_dict[grid_str])
            break
        else:
            seen.add(grid_str)

# We will see the same setup at i= 416, 444,... (i starts at zero)

# thus we can first take 416 steps, then skip quite a lot
# 416 + x*28 = 1_000_000_000
# x = (1_000_000_000 - 416) / 28 = 35714270.85714286
# the decimal part corresponds to 24 steps
# so take 416 + 24 = 440 steps and then check the resource value. This should match to res.value after 1_000_000_000 minutes

print("\n\nGetting resource value after 1000000000 minutes...")
grid = step(grid_init, 440, show_grid=False)
print("Resource value after 1000000000 minutes: ", get_resource_value(grid))
# 195776 is the right answer
