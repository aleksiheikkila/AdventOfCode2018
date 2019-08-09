"""
Advent of code, 2018
Day 12: Subterranean Sustainability
Not that great performancewise. Would be better to represent plants/state in some other way than as a string
E.g. state as a set of plant location integer indexes, getting rid of string operations + rebuilding strings
"""

from typing import Dict

NUM_GENERATIONS = 20
RULE_LEN = 5

# TEST DATA (should implement this "parse" as a function
RAW = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

INPUT_TEST = [line.strip("\n").strip() for line in RAW.split("\n")]

initial_state_test = INPUT_TEST[0].replace("initial state: ", "")
rules_test = {}
for rule in INPUT_TEST[2:]:
    left, right = rule.split(" => ")
    rules_test[left] = right


# ACTUAL PROBLEM DATA
with open("data/day12.txt") as f:
    input = [line.strip("\n").strip() for line in f]


initial_state = input[0].replace("initial state: ", "")
print("init state: ", initial_state)

rules = {}
for rule in input[2:]:
    left, right = rule.split(" => ")
    rules[left] = right


# Part A:
# After 20 generations, what is the sum of the numbers of all pots which contain a plant?

class Plantation():       
    def __init__(self, state: str, rules: Dict[str, str]):
        self.left_idx = 0
        self.generation = 0
        self.rules = rules
        
        self.state = state 
        self.next_state = None
        self.pad_state()
        
    def evolve(self, num_gens: int = 1):
            
            next_state = self.state
            
            # Start from the left. Apply all filters. When match, replace and move one step to right
            for i in range(len(self.state) - RULE_LEN):
                block = self.state[i:i+RULE_LEN]
                for pattern, replacement in self.rules.items():
                    if block == pattern:
                        #replace and break
                        next_state = next_state[:i+2] + replacement + next_state[i+3:]
                        break  # break the pattern matching for this location
                        
            self.state = next_state
            self.pad_state()
            self.generation += 1    
                
            
    def __repr__(self):
        return f"gen:{self.generation}, left_idx:{self.left_idx}\n{self.state}"
        
        
    def get_score(self):
        score = 0
        for i, char in enumerate(self.state):
            if char == "#":
                score += i + self.left_idx
        
        return score
        

    def pad_state(self):
        """
        pads state from both ends with dots, so that the state has "room" to grow beyond initial borders
        """
        # Left hand side
        first_plant_idx = self.state.find("#")  # index in the list... not as in problem... 1
        pad_amount_left = 5 - first_plant_idx if first_plant_idx <= 4 else 0
        
        # right hand side
        last_plant_idx = self.state.rfind("#")
        pad_amount_right = 6 + last_plant_idx - len(self.state) if len(self.state) - last_plant_idx < 6 else 0
        
        # update
        self.state = ("." * pad_amount_left) + self.state + ("." * pad_amount_right)
        self.left_idx -= pad_amount_left


#p_test = Plantation(state=initial_state_test, rules=rules_test)
#print(p_test)
#p_test.evolve(2)
#print(p_test)


p = Plantation(state = initial_state, rules = rules) 
#print(p.state)
#print(p)
p.evolve(20)

print(p.left_idx)
print(p.state)

score = p.get_score()
print(score)
# 3738 is the right answer


# PART B:
# After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
# Okay, that's newer gonna finish. Not with the current implementation, and not even with a faster implementation...
# There gotta be a pattern to be found

p_b = Plantation(state = initial_state, rules = rules) 

# TRY TO FIND THE PATTERN!

# Possibilities could include:
# We see the exact same state again --> deterministic --> would start to loop
# There is some pretty clear pattern in how the new plants emerge, or how the score changes over time

# Lets see what happens to the score over time. Get score and delta score per generation

scores = {}
scores[p_b.generation] = p_b.get_score()
for _ in range(300):
    p_b.evolve()
    scores[p_b.generation] = p_b.get_score()
    print(p_b.generation, p_b.get_score(), "score delta: ", scores[p_b.generation] - scores[p_b.generation - 1])
    
# We find that starting from gen 100, the score delta is constant 78
# At gen 1000, score is 80467
# Now, after 50 bil gens the score will be:
# 80467 + (50_000_000_000 - 1_000) * 78
print("Score after 50 billion generations:", str(80467 + (50_000_000_000 - 1_000) * 78))
# Answer is: 3900000002467
