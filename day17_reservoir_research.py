"""
Advent of code, 2018
Day 17: Reservoir Research
---
This ended up being a bit more involved. This proceeds naively, starting each time from the water source. 
Before some late stage changes I had a logic that set the source for new block of water to be closer to the frontier.
Did not care to rewrite it
"""

RAW_TEST = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

import re
from typing import Tuple, Dict

CLAY = "#"
WATER_SPRING = (500, 0)  # x, y

# Type hints:
Pos = Tuple[int, int]  # x and y
Grid = Dict[Pos, str]  # position -> what the "map" looks like. Map is sparse, not containing sand "."

# input format: x or y = something, other = something1...something2
rgx = "([xy])=(\d+), ([xy])=(\d+)..(\d+)"

def generate_grid(inp:str) -> Grid:
    """
    Arguments:
        inp {str} -- THe raw unsplitted test giving the "map"
    
    Returns:
        Grid -- where Pos (XY) is the key, value: the corresponding char on the map
    """
    # grid has sparse representation. Not storing the sand "." positions
    grid = {}

    lines = inp.splitlines()

    for line in lines:
        lname, lval, rname, rightlo, righthi = re.match(rgx, line).groups()
        
        if lname == "x" and rname == "y":
            for rval in range(int(rightlo), int(righthi)+1):
                grid[(int(lval), rval)] = CLAY
        elif lname == "y" and rname == "x":
            for rval in range(int(rightlo), int(righthi)+1):
                grid[(rval, int(lval))] = CLAY
        else:
            raise ValueError("Unexpected input")

    # There is also a spring of water ("+") near the surface at x=500, y=0
    grid[WATER_SPRING] = "+"

    return grid


def show(grid: Grid) -> str:
    x_lo = min(x for x, y in grid.keys())
    x_hi = max(x for x, y in grid.keys())
    y_lo = min(y for x, y in grid.keys())
    y_hi = max(y for x, y in grid.keys())

    # if position does not contain anything in the grid, it's sand "."
    rows = [[grid.get((x, y), '.') 
            for x in range(x_lo, x_hi + 1)]
            for y in range(y_lo, y_hi + 1)]

    return "\n".join(''.join(row) + f"\t{rowno}" for rowno, row in enumerate(rows))


def count_squares_reached_by_water(grid: Grid) -> int:
    # Need to consider only between those y for which we had those probing results (i.e. CLAY)
    y_low  = min(y for (x, y), val in grid.items() if val == CLAY)
    y_high = max(y for (x, y), val in grid.items() if val == CLAY)

    return len([v for (x,y), v in grid.items() if v in ("~", "|", "b", "/") and y >= y_low and y <= y_high])


def count_squares_with_standing_water(grid: Grid) -> int:
    # Need to consider only between those y for which we had those probing results (i.e. CLAY)
    y_low  = min(y for (x, y), val in grid.items() if val == CLAY)
    y_high = max(y for (x, y), val in grid.items() if val == CLAY)
    
    return len([v for (x,y), v in grid.items() if v == "~" and y >= y_low and y <= y_high])

# define a func for the water flow.
# rules. Put one unit in:
# Always fall straight down, as far as possible. except when blocked (by clay or water)
# when blocked: first go left as far as possible.
# Until cannot move any more (then you can put in the next unit of water)

# determine when to stop: when new unit is put in and it falls out of the grid

def flow(grid: Grid, units=None) -> None:
    """
    flow water units one by one until finished.
    """
    seq = 0  # water unit nbr, for printing of progress

    if not units:
        continue_pos = None  # NO LONGER IN USE. restart the flow closer to the frontier
        while True:
            if seq % 100 == 0: print(seq)

            ret = flow_one(grid, start_pos=continue_pos)
            if ret == True:
                show(grid)
                break
            
            #continue_pos = ret[1] if ret[1] is not None else None
            seq += 1


    else:  # pour in just "units" units of water
        continue_pos = None  # not in use
        for unit in range(units):
            if unit % 100 == 0: print(unit)
            ret = flow_one(grid, start_pos=continue_pos)

            #if len(ret) > 1:
            #    continue_pos = ret[1] if ret[1] is not None else None


def set_slash_ifnot_bar(grid: Grid, pos: Pos):
    # do not replace "|" with "/"... for the internal logic to work
    if grid.get(pos, ".") != "|":
        grid[pos] = "/"


def flow_one(grid: Grid, start_pos:Pos = None):
    """
    
    Arguments:
        grid {Grid} -- [grid]
    
    Keyword Arguments:
        start_pos {Pos} -- [where to start the water flow. NO LONGER USED] (default: {None})
    
    Returns:
        True -- When all is done, water has made every point wet that it can
        (xi,yi), (xs,ys)  --  tuple of the location where the water unit ended up, 
                                tuple with new start position for the next water unit (NO LONGER USED)

    "~" denotes standing water
    "|" denotes falling water / also the place where the falling water hits obstacle
    "/" denotes running water (water that cannot / has not settled)
    "b" denote running water, but it also means "block", a direction where we do not need to go 
        (exhausted direction, where water will just pour out of the grid without touching any new points)
        "b" also ensure that flowing water end up going both left and right
    """

    # Where to start (NO LONGER IN USE; start from the water source each time)
    if not start_pos:
        curr_x, curr_y = WATER_SPRING
    else:
        if grid.get(start_pos, ".") != "~":
            curr_x, curr_y = start_pos
        else:
            curr_x, curr_y = WATER_SPRING


    # NO LONGER IN USE
    suggested_start_pos = [None, (curr_x, curr_y)]  # use instead of WATER_SPRING to save unnecessary compute

    num_bouncebacks = 0  # how many times the water has bounced back from obstacle (within the same level y)
    direction = "down"


    # Merkataan: "/" vaakasuunnassa vellova vesi
    # "b" blokkaa sellaisen vuon joka menee ulos gridistä. Tarvitaan prev turn pos
    prev_turn_loc = None

    # Strategy:
    # 1. katso aina ensin pääseekö alas (pääsee ellei alapuolella CLAY tai ~), mene jos pääsee
    # 2. jos ei pääse ja putoaminen loppuu, katso onko oikealla puolella blokki.
    #   2a) jos on, lähde vasemmalle. Samassa tasossa olevan esteen koittaessa --> ~
    #   2b) jos ei ole, lähde vasemmalle, mutta edellytä samassa tasossa bounceback (vas vas vas, oho este, oik oik oik)
    #       oikealle tullessa este --> ~
    #  | muuttuu ~ vasta kun mol. puolilla joko # tai ~
    # pidä kirjaa missä viimeksi käännös. Jos päätyy ulos gridistä, aseta sinne blockki b
    # loppuu kun vesi tippuu kohtaan jossa molemmilla puolilla blocki, tai toisella blocki ja toisella #

    # take one step at a time
    while True:
        # case out of grid
        if curr_y > y_hi or curr_y < y_lo:
            # water flowed out of the grid... block the prev turn location with "b" so that we do not end up here any more
            print("OUT OF BOUNDS", curr_x, curr_y)
            print("Setting b on", prev_turn_loc)
            if not prev_turn_loc:
                # this is the "finished" criterion. This will happen at the top of the grid. -> whole grid exhausted
                return True 
            else:
                grid[prev_turn_loc] = "b"
                return (curr_x, curr_y), suggested_start_pos[0]

        # case water can fall down
        if grid.get((curr_x, curr_y+1), ".") in (".", "|", "/"):
            if direction != "down":  # just started to go down
                suggested_start_pos.pop(0)  # remove leftmost
                suggested_start_pos.append((curr_x, curr_y+1))   # NO LONGER IN USE
            grid[(curr_x, curr_y+1)] = "|"
            curr_x, curr_y = curr_x, curr_y+1
            num_bouncebacks = 0  # this is level-specific -> reset
            direction = "down"
            continue

        # case goind down but there is a flowing water with a block "b" below
        if direction == "down" and grid.get((curr_x, curr_y+1), ".") == "b":
            # no need to continue. Already processed appropriately
            if not prev_turn_loc:
                # finished criterion
                return True 
            else:
                # set block to the previous turn
                grid[prev_turn_loc] = "b"
                return (curr_x, curr_y), None  # start from beginning

        # case was falling down, blocked below and from both sides, with at least on side with "b" 
        # --> then all water will just pour out of the grid. Set block "b" to prev turn
        if (direction == "down"
            and grid.get((curr_x, curr_y+1), ".") not in (".", "|")
            and grid.get((curr_x-1, curr_y), ".") in (CLAY, "~", "b")
            and grid.get((curr_x+1, curr_y), ".") in (CLAY, "~", "b")
            and (grid.get((curr_x-1, curr_y), ".") == "b" or grid.get((curr_x+1, curr_y), ".") == "b")):

            if not prev_turn_loc:
                # all done
                return True
            else:
                grid[prev_turn_loc] = "b"

            return (curr_x, curr_y), None  # start from beginning

        # case was going down, now down direction is blocked
        if direction == "down" and grid.get((curr_x, curr_y+1), ".") not in (".", "|"):
            # case blocked from both sides"
            if grid.get((curr_x-1, curr_y), ".") in (CLAY, "~") and grid.get((curr_x+1, curr_y), ".") in (CLAY, "~"):  # oli "b"
                # blocked from both sides --> "|" becomes "~"
                grid[(curr_x, curr_y)] = "~"
                return (curr_x, curr_y), suggested_start_pos[0]
            elif grid.get((curr_x-1, curr_y), ".") in (CLAY, "~", "b"):
                # left blocked, go right
                if grid.get((curr_x-1, curr_y), ".") == "b": 
                    max_bouncebacks = 99  # essentially: cannot become standing water as there is route to out of grid
                else: 
                    max_bouncebacks = 0  # when encounters next obstacle, can form standing water
                direction = "right"
                prev_turn_loc = (curr_x+1, curr_y)
                set_slash_ifnot_bar(grid, (curr_x+1, curr_y))
                curr_x, curr_y = curr_x+1, curr_y
            elif grid.get((curr_x+1, curr_y), ".") in (CLAY, "~", "b"):
                # right blocked, go left
                if grid.get((curr_x+1, curr_y), ".") == "b":
                    max_bouncebacks = 99  # essentially: cannot become standing water as there is route to out of grid
                else:
                    max_bouncebacks = 0  # when encounters next obstacle, can form standing water
                direction = "left"
                prev_turn_loc = (curr_x-1, curr_y)
                set_slash_ifnot_bar(grid, (curr_x-1, curr_y))
                curr_x, curr_y = curr_x-1, curr_y
           
            # else go left and require bounceback (do not form standing water when obstacle is encountered, switch dir instead)
            else:
                max_bouncebacks = 1
                direction = "left"
                prev_turn_loc = (curr_x-1, curr_y)
                set_slash_ifnot_bar(grid, (curr_x-1, curr_y))
                curr_x, curr_y = curr_x-1, curr_y
            
            continue

        # going left, can continue
        if direction == "left" and grid.get((curr_x-1, curr_y), ".") not in (CLAY, "~"):
            set_slash_ifnot_bar(grid, (curr_x-1, curr_y))
            curr_x, curr_y = curr_x-1, curr_y
            continue

        # going left but blocked
        if direction == "left" and grid.get((curr_x-1, curr_y), ".") in (CLAY, "~"):
            # depends on max_bouncebacks
            if num_bouncebacks >= max_bouncebacks:
                # okay, forms standing water
                grid[(curr_x, curr_y)] = "~"
                return (curr_x, curr_y), suggested_start_pos[0]
            else:
                # bounce back, do not yet form standing water
                num_bouncebacks += 1
                direction = "right"
                continue

        # going right, can continue
        if direction == "right" and grid.get((curr_x+1, curr_y), ".") not in (CLAY, "~"):
            set_slash_ifnot_bar(grid, (curr_x+1, curr_y))
            curr_x, curr_y = curr_x+1, curr_y
            continue

        # going right but blocked
        if direction == "right" and grid.get((curr_x+1, curr_y), ".") in (CLAY, "~"):
            if num_bouncebacks >= max_bouncebacks:
                # form standing water
                grid[(curr_x, curr_y)] = "~"
                return (curr_x, curr_y), suggested_start_pos[0]
            else:
                # do not yet form standing water but switch direction
                num_bouncebacks += 1
                direction = "left"
                continue



# UNIT TEST CASE:
grid = generate_grid(RAW_TEST)

# Only consider what happens between:
y_lo = min(y for x, y in grid.keys())
y_hi = max(y for x, y in grid.keys())

flow(grid)
print(show(grid))
print("Water count: ", count_squares_reached_by_water(grid))
assert count_squares_reached_by_water(grid) == 57
assert count_squares_with_standing_water(grid) == 29


# PART 1:
# How many tiles can the water reach within the range of y values in your scan?

with open("data/day17.txt") as f:
    actual_input = f.read()

act_grid = generate_grid(actual_input)

# Only consider what happens between:
y_lo = min(y for x, y in act_grid.keys())
y_hi = max(y for x, y in act_grid.keys())

flow(act_grid)
print(show(act_grid))
print("Water count (wet tiles): ", count_squares_reached_by_water(act_grid))
# Your puzzle answer was 31383


####################
# PART 2:
# how many tiles contain water after the fountain runs out of water
# --> only those ~ will stay
print("Stading water count: ", count_squares_with_standing_water(act_grid))
# Your puzzle answer was 25376