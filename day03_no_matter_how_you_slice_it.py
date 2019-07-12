"""
Advent of code, 2018
Day 3: No Matter How You Slice It
"""

import re
from collections import Counter

regex = "#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"  # to grab the data from claim string

class Rectangle():
    
    def __init__(self, id, x_lo, y_lo, x_hi, y_hi):
        self.id = id
        self.x_lo = x_lo
        self.y_lo = y_lo
        self.x_hi = x_hi
        self.y_hi = y_hi
    
    @staticmethod
    def generate_from_claim(claim):
        """
        returns a Rectangle object, generated from a single claim string
        """
        id, x_lo, y_lo, width, height = (int(elem) for elem in re.match(regex, claim).groups())
        return Rectangle(id, x_lo, y_lo, x_lo + width, y_lo + height)
    
    def yield_all_squares(self):
        """
        generator to yield all inch-by-inch coordinates (squares) of the Rectangle (the upper left corner coordinates of the square, actually)
        """
        for x in range(self.x_lo, self.x_hi):
            for y in range(self.y_lo, self.y_hi):
                yield(x,y)
    

def coverage(rectangles):
    """
    returns a Counter containing the num of squares at each coordinate (upper left corner coords)
    """
    counts = Counter()
    
    for rectangle in rectangles:
        for coord in rectangle.yield_all_squares():
            counts[coord] += 1  # default value of everything is zero
    
    return counts

def num_squares_with_overlap(claims):
    """
    returns the num of squares with multiple overlapping claims
    """
    rectangles = [Rectangle.generate_from_claim(claim) for claim in claims]
    counts = coverage(rectangles)
    
    return len([count for count in counts.values() if count >= 2])


# Part 1:
# data format: #1263 @ 488,932: 15x17
with open("data/day03.txt") as f:
    claims = [line.strip() for line in f]

# How many square inches of fabric are within two or more claims?
print(num_squares_with_overlap(claims))


# Part 2:
# exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. Its id?

def non_overlapping_claim(claims):
    """
    returns the id of the only entirely non-overlapping claim
    """
    rectangles = [Rectangle.generate_from_claim(claim) for claim in claims]
    counts = coverage(rectangles)
    
    
    nonoverlapping_rectangle = [rectangle 
                                for rectangle in rectangles 
                                if all(counts[coord] == 1 for coord in rectangle.yield_all_squares())]
    
    assert len(nonoverlapping_rectangle) == 1
    
    return nonoverlapping_rectangle[0].id


print(non_overlapping_claim(claims))

# Unit test
TEST_CLAIMS = [
    "#1 @ 1,3: 4x4",
    "#2 @ 3,1: 4x4",
    "#3 @ 5,5: 2x2",
    ]

assert non_overlapping_claim(TEST_CLAIMS) == 3