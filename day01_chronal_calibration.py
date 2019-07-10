"""
Advent of code, 2018
Day 01 chronal calibration
"""

# Part 1:
with open("data/day01.txt") as f:
    changes = [int(line.strip()) for line in f]
    
print(sum(changes))


# Part 2:
def first_repeat_freq(numbers):
    """
    Returns the first encountered repeating frequency
    Loops the list over as many times as needed
    """
    freq = 0
    seen = {freq}
    
    # Loop the list many times over if needed
    while True:
        for change in numbers:
            freq += change
            
            if freq in seen:
                return freq
            else:
                seen.add(freq)
                
        
print(first_repeat_freq(changes))


# Provided unit tests
assert first_repeat_freq([1, -1]) == 0
assert first_repeat_freq([3, 3, 4, -2, -4]) == 10
assert first_repeat_freq([-6, 3, 8, 5, -6]) == 5
assert first_repeat_freq([7, 7, -2, -7, -4]) == 14
