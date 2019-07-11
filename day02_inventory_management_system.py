"""
Advent of code, 2018
Day 02 Inventory Management System
"""

from collections import Counter

# Part 1:
with open("data/day02.txt") as f:
    ids = [line.strip() for line in f]
    
#print(ids[0])

# ...counting the number (of ids) that have an ID containing exactly two of any letter 
# and then separately counting those with exactly three of any letter. 
# (does not matter how many times these occur above 0/1 threshold)
# You can multiply those two counts together to get a rudimentary checksum and compare it to what your device predicts.

def char_counts(word):
    """
    Given a word (str), returns the unique char counts in that word as a set
    """
    
    char_counts = Counter(word)
    return set(char_counts.values())

def calc_checksum(ids):
    """
    Returns 
    (num ids with some (one or many) chars occuring exactly twice) * (num ids with some (one or many) chars occuring exactly three times)
    """
    num_twos = 0
    num_threes = 0
    
    for id in ids:
        ccounts = char_counts(id)
        
        if 2 in ccounts:
            num_twos += 1
        if 3 in ccounts:
            num_threes += 1
        
    return num_twos * num_threes

# Provided unit tests
assert calc_checksum([
    "abcdef",
    "bababc",
    "abbcde",
    "abcccd",
    "aabcdd",
    "abcdee",
    "ababab"
]) == 12

print(calc_checksum(ids))

# Part 2:   
# The boxes will have IDs which differ by exactly one character at the same position in both strings
# What letters are common between the two correct box IDs?

# approach: remove each character from each id, count... which one gets two hits


def chars_in_common(ids):
    """
    returns a string where the common characters are as a string (the removed char placeholder "_" removed)
    Returns as soon as two ids that differ exactly by one char (in the same position) are found
    """
    ids_with_one_char_removed = dict()

    for id in ids:
        for i in range(len(id)):
            # for each id, remove each char
            id_one_char_removed = tuple(id[:i] + "_" + id[i+1:])  # tuple splits this str to chars
            
            # increment the count
            ids_with_one_char_removed[id_one_char_removed] = ids_with_one_char_removed.get(id_one_char_removed, 0) + 1
            
            if ids_with_one_char_removed[id_one_char_removed] == 2:
                return "".join([char for char in id_one_char_removed if char != "_"])


print(chars_in_common(ids))

# Provided unit tests
TEST_IDS = [
    "abcde",
    "fghij",
    "klmno",
    "pqrst",
    "fguij",
    "axcye",
    "wvxyz"
]

assert chars_in_common(TEST_IDS) == "fgij"
