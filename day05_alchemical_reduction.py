"""
Advent of code, 2018
Day 5: Alchemical Reduction 
"""

# alternative... regex?

# seems recursive, but (naive implementation) runs over the set max depth 
# so lets just loop...
def reduce_polymer(polymer):
    id = 0
    reduced_polymer = polymer
    
    while id < len(reduced_polymer) - 1:
        if reduced_polymer[id].upper() == reduced_polymer[id+1].upper():    # same char, maybe different size
            
            if reduced_polymer[id] == reduced_polymer[id+1]:    ## same size as well -> does not react
                id += 1
                continue
            else:  # different char sizes -> reacts
                # reduce (drop id and id+1 chars), then backtrack id by one to allow further collapsing
                reduced_polymer = reduced_polymer[:id] + reduced_polymer[id+2:]
                id = max(id - 1, 0)   # handle the case of running into negative indexes
                continue
        id += 1
    
    
    return reduced_polymer
        


#How many units remain after fully reacting the polymer you scanned?

with open("data/day05.txt") as f:
    polymer = f.read()
    
reduced = reduce_polymer(polymer)

# this is the answer:
print(len(reduced))

# unit test
TEST_POLYMER = "dabAcCaCBAcCcaDA"

assert reduce_polymer(TEST_POLYMER) == "dabCBAcaDA"
assert len(reduce_polymer(TEST_POLYMER)) == 10



#########
# Part B:
# One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. 
# Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), 
# fully react the remaining polymer, and measure its length.

diff_chars = set(polymer.upper())

poly_lengths = dict()

# Strategy: remove each char (case insensitive) one by one, reduce polymer, log the length of the resulting polymer
for rem_char in diff_chars:
    manipulated_polymer = polymer.replace(rem_char, "").replace(rem_char.lower(), "")
    reduced_polymer = reduce_polymer(manipulated_polymer)
    poly_lengths[rem_char] = len(reduced_polymer)


# the best char to rem, that results into shorters polymer, is:
best_char_to_remove = min(poly_lengths, key=poly_lengths.get)  # returns the key

# resulting reduced polymer length:
print(poly_lengths[best_char_to_remove])
