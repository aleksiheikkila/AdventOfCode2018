"""
Advent of code, 2018
Day 15: Beverage Bandits
This is incomplete. This solution seemed to give to correct answer to both the given test cases and some other input
data I managed to found. However, it does not give the correct answer for my input (or at least the grader does not agree).
Could be some extreme corner case that I am missing.
"""

import networkx as nx

from typing import Dict, List, Tuple, NamedTuple, Set


class Pos(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> List["Pos"]:
        x, y = self.x, self.y
        yield from [Pos(x-1, y), Pos(x+1, y), Pos(x, y-1), Pos(x, y+1)]


    def manhattan_dist(self, other: "Pos") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Creature:
    def __init__(self, id: int, species: str, pos: Pos, att_pwr: int = 3, hp: int = 200):
        self.id = id
        self.species = species
        self.att_pwr = att_pwr
        self.hp = hp
        self.pos = pos
        self.dead = False  

    def attack(self, other: "Creature"):
        other.hp -= self.att_pwr
        if other.hp <= 0:
            other.dead = True

    def move(self, to: Pos):
        self.pos = to

    def __repr__(self):
        return f"{self.species}(id:{self.id}) at {self.pos} - hp:{self.hp}"

    def dist(self, other):
        return self.pos.manhattan_dist(other.pos)


class Battle():
    def __init__(self, _map: Dict[Pos, str], creatures: List[Creature]):
        self._map = _map
        self.x_max = max(position.x for position in self._map.keys())
        self.y_max = max(position.y for position in self._map.keys())
        self.creatures = creatures
        self.round = 0
        self.generate_graph()

    def sum_hp_left(self):
        return sum(creature.hp for creature in self.creatures if not creature.dead)

    def get_outcome(self):
        return (self.round - 1) * self.sum_hp_left()

    def generate_graph(self):
        # there really isnt need to rebuild the graph every time from scratch... but this will do for now
        G = nx.DiGraph()

        for pos, terrain in self._map.items():
            x, y = pos.x, pos.y
            if terrain in (".", "G", "E"):  # start node
                if x+1 <= self.x_max and self._map[Pos(x+1, y)] == ".":
                    G.add_edge(pos, Pos(x+1, y))
                if x-1 >= 0 and self._map[Pos(x-1, y)] == ".":
                    G.add_edge(pos, Pos(x-1, y))
                if y+1 <= self.y_max and self._map[Pos(x, y+1)] == ".":
                    G.add_edge(pos, Pos(x, y+1))
                if y-1 >= 0 and self._map[Pos(x, y-1)] == ".":
                    G.add_edge(pos, Pos(x, y-1))

        self.graph = G


    def step(self, num_rounds: int = 1):
        for _ in range(num_rounds):
            self.round += 1
            #print(f"============================\nRound {self.round} begins!") 

            # determine the order
            self.creatures.sort(key = lambda creature: (creature.pos.y, creature.pos.x))

            for curr_creature in self.creatures:
                print(f"{curr_creature.species} Creature {curr_creature.id} starts turn", curr_creature)

                if curr_creature.dead:
                    #print("...killed creature does not do anything")
                    continue

                # identify alive opponent targets
                targets = [c for c in self.creatures if c.species != curr_creature.species and not c.dead]
                
                # if no targets, combat ends
                if len(targets) == 0:
                    print("NO TARGETS - BATTLE ENDS!")
                    return True

                # Am I already in attack range for some target? If yes, do not move, ATTACK
                within_att_range = [target for target in targets if curr_creature.dist(target) == 1]

                try_moving = True if len(within_att_range) == 0 else False

                if try_moving:
                    # Else identify open squares around targets
                    # for each target, check which of the four neighb slots are valid (open) destinations
                    possible_destinations = [adj_pos for target in targets
                                            for adj_pos in target.pos.neighbors()
                                            if self._map.get(adj_pos, None) == "."]

                    # if no open squares, unit's turn ends (no one within attack range, as it was checked before)
                    if len(possible_destinations) == 0:
                        continue

                    # If open squares adj to target, unit tries to move to one of those
                    # Which in-range square can be reached with fewest steps? Choose that to target. 
                    # If no cannot be reached, do not move

                    # Rebuild graph
                    self.generate_graph()

                    #print("Seaching for the shortest paths")
                    
                    # sort possible_destinations by naive manhattan distance (to asc order)
                    possible_destinations.sort(key=lambda dest_pos: curr_creature.pos.manhattan_dist(dest_pos))
                    
                    len_shortest_path = float("Inf")  # shortest path found so far
                    paths = []

                    # If current Pos is not in the graph (= the current creature is blocked) -> cannot move, and cannot attack
                    if curr_creature.pos not in self.graph: continue

                    # First, use much lighter nx.shortest_path to get one of the (usually many) shortest paths to each destination.
                    # Use this to get the shortest path lenght for that destination.
                    # Then only for destination(s) that actually have the shortest path, get all shortest paths
                    # and get the one matching the "reading order" condition
                    
                    sp_to_dest_poss = []  # tuple of dest_pos, path_len
                    for dest_pos in possible_destinations:
                        if dest_pos in self.graph and nx.has_path(self.graph, curr_creature.pos, dest_pos):
                            sp_to_dest_poss.append((dest_pos, len(nx.shortest_path(self.graph, curr_creature.pos, dest_pos))))
                            # some shortest path... though not really path length here, because first element is the start pos
                    
                    if len(sp_to_dest_poss) == 0: continue   # couldnt move, couldn yet attack

                    # get the shortest path(s) lenght
                    sp_to_dest_poss.sort(key=lambda x: x[1])
                    min_sp_dist = sp_to_dest_poss[0][1]
                    
                    # generate the set of destinations positions for which we need all shortest paths
                    candidate_pos_for_further_sp_analysis = [pos for (pos, dist) in sp_to_dest_poss if dist <= min_sp_dist]

                    for dest_pos in candidate_pos_for_further_sp_analysis:
                        if (curr_creature.pos.manhattan_dist(dest_pos) <= len_shortest_path and
                        dest_pos in self.graph
                        and nx.has_path(self.graph, curr_creature.pos, dest_pos)):

                            paths.extend(list(nx.all_shortest_paths(self.graph, curr_creature.pos, dest_pos)))
                            
                            # this shortest path tracking / prefiltering is unnecessary here - it has been taken care already
                            min_len = min(map(len, paths))
                            if min_len < len_shortest_path:
                                len_shortest_path = min_len

                    #print(paths)
                    #print("Done seaching for the shortest paths")

                    if len(paths) < 1:
                        print("Nowhere to go")
                        # do not move
                        continue

                    # Chose the path along which to step. Shortest + "reading order"
                    paths.sort(key=lambda path: (len(path), path[1].y, path[1].x))
                    chosen_path = paths[0]
                    next_pos = chosen_path[1]

                    # Move and update map (poorly structured...)
                    self._map[curr_creature.pos] = "."
                    curr_creature.move(next_pos)
                    self._map[curr_creature.pos] = curr_creature.species  # "E" or "G"

                    #print("Pos after moving:", curr_creature.pos)

                # Then try to attack
                within_att_range = [target for target in targets if curr_creature.dist(target) == 1]

                if len(within_att_range) > 0:
                    # if many targets within range, which one to attack?
                    # the adjacent target with the fewest hit points is selected
                    # in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.
                    within_att_range.sort(key=lambda target: (target.hp, target.pos.y, target.pos.x))
                    chosen_target = within_att_range[0]
                    curr_creature.attack(chosen_target)
                    if chosen_target.dead:
                        #print("Target dead:", chosen_target)
                        self._map[chosen_target.pos] = "."

        # out of steps loop
        return False


    def fight_until_end(self):
        while True:
            if self.step(): break

        print(f"Battle end after {self.round-1} full rounds")
        print(self.creatures)
        print("Sum HP left:", self.sum_hp_left())
        print("Outcome:", self.get_outcome())

        return self.get_outcome()


    def show_map(self):
        """
        prints the current map (including creatures)
        """
        map_str = ""
        for y in range(self.y_max+1):
            line = ""
            for x in range(self.x_max+1):
                line += self._map[Pos(x,y)]
            line += "\n"
            map_str += line

        print(map_str)


    def show_terrain_map(self):
        """
        prints the current terrain map (map without creatures)
        """
        map_str = ""
        for y in range(self.y_max):
            line = ""
            for x in range(self.x_max):
                line += self._map[Pos(x,y)] if self._map[Pos(x,y)] not in ("G", "E") else "."
            line += "\n"
            map_str += line

        print(map_str)


    @staticmethod
    def parse_initial_state(init_input: str) -> "Battle":
        lines = [line for line in init_input.splitlines()]
        # top left = Pos(0,0)
        _map = {Pos(x, y): elem
                for y, line in enumerate(lines)
                for x, elem in enumerate(line)
               }

        creatures = [(elem, Pos(x,y))
                    for y, line in enumerate(lines)
                    for x, elem in enumerate(line) if elem in ("G", "E")
                    ]
        creatures = [Creature(id, *creature) for id, creature in enumerate(creatures)]

        return Battle(_map=_map, creatures=creatures)


with open("data/day15.txt") as f:
    init_input = f.read()


# Movement test:
RAW = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""

tb = Battle.parse_initial_state(RAW)

# UNIT TESTS:

RAW2 = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""


# Unit tests:
tb2 = Battle.parse_initial_state(RAW2)
assert tb2.fight_until_end() == 27730

RAW3 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""

tb3 = Battle.parse_initial_state(RAW3)
assert tb3.fight_until_end() == 36334


RAW4 = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""

tb4 = Battle.parse_initial_state(RAW4)
assert tb4.fight_until_end() == 39514


RAW5 = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""

tb5 = Battle.parse_initial_state(RAW5)
assert tb5.fight_until_end() == 27755


RAW6 = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""

tb6 = Battle.parse_initial_state(RAW6)
assert tb6.fight_until_end() == 28944


RAW7 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""

tb7 = Battle.parse_initial_state(RAW7)
assert tb7.fight_until_end() == 18740


# All unit test pass!

# Other input data found on the web
#with open("data/day15_other.txt") as f:
#    some_other_test_case = f.read()

#ob = Battle.parse_initial_state(some_other_test_case)
#outcome = ob.fight_until_end()
#print("Outcome:", outcome)
# Outcome: 246176  after 98 full rounds. 
# So, SOLUTION OK FOR THIS PROBLEM INPUT AS WELL!


# Yet another full problem input
with open("data/day15_other2.txt") as f:
    some_other_test_case2 = f.read()

#ob2 = Battle.parse_initial_state(some_other_test_case2)
#outcome2 = ob2.fight_until_end()
#print("Outcome:", outcome2)
# Fight over at round 71, goblins won with 2775 pts remaining, result = 197025.
# OK, GOT THIS AS WELL!



# Then the actual input:
b = Battle.parse_initial_state(init_input)
outcome = b.fight_until_end()
print("Outcome:", outcome)
# Outcome: 201411  -- too high!
# THERE IS SOMETHING THAT I DID NOT CATCH / SOMETHING MYSTIC WITH MY OWN INPUT...
# the solution seems to work for every other case

