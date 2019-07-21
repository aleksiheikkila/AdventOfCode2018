"""
Advent of code, 2018
Day 6: Chronal Points 
"""

# Part A:
# Using only the Manhattan distance, determine the area around each Point by counting the number of integer X,Y locations that are closest to that Point 
# (and aren't tied in distance to any other Point).

# Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of Points:


from collections import Counter
from typing import NamedTuple, List, Dict


class Point(NamedTuple):
    """
    Point with x and y coordinates
    """
    x: int
    y: int

    @staticmethod
    def from_line(line: str) -> 'Point':
        x, y = line.split(", ")
        
        return Point(int(x), int(y))
        
    def manhattan_distance_to(self, other: 'Point') -> int:
        """
        returns manhattan distance from this instance to other Point
        """
        return abs(self.x - other.x) + abs(self.y - other.y)
        
    def total_manhattan_distance(self, others: List['Points']) -> int:
        """
        given a Point, give the sum on M distance to all (other) points
        """
        # sum of a generator object. Not actually 'others', but since the dist to self = zero -> equivalent
        return sum(self.manhattan_distance_to(point) for point in others)
        
        

def get_nearests_grid(points: List[Point]) -> Dict[Point, int]:
    """
    returns a dict that contains the Points on a grid as keys and the index of the nearest Point in each grid slot (None if tied).
    It's enough to consider the grid delineated by the extreme coordinates of the set of points
    """
    x_min = min(point.x for point in points)
    x_max = max(point.x for point in points)
    y_min = min(point.y for point in points)
    y_max = max(point.y for point in points)
    
    print(x_min, x_max, y_min, y_max)
    
    nearests = {}
    
    # loop thru the grid, get the nearest one
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            ref_point = Point(x, y)
            distances = [(i, ref_point.manhattan_distance_to(point)) for i, point in enumerate(points)]
            
            # sort by the distance, ascending
            distances.sort(key = lambda tup: tup[1])
            
            # tied case, None as value:
            if distances[0][1] == distances[1][1]:
                nearests[ref_point] = None
            else: # non tied case. Value is the idx of the nearest Point
                nearests[ref_point] = distances[0][0]
   
    return nearests


def calc_areas(grid: Dict[Point, int]) -> int:
    """
    returns Counter of ints
    """
    x_min = min(point.x for point in grid)
    x_max = max(point.x for point in grid)
    y_min = min(point.y for point in grid)
    y_max = max(point.y for point in grid)
    
    # get the indexes of those points that are the nearests on the border
    # these and only these are the points that have infinite area associated with them --> ignore these
    idx_on_boundary = set()
    
    for point, idx in grid.items():
        if point.x in (x_min, x_max) or point.y in (y_min, y_max):
            idx_on_boundary.add(idx)
    
    print(idx_on_boundary)    
    areas = Counter()
    
    for point, idx in grid.items():
        if idx not in idx_on_boundary:
            areas[idx] += 1   # Counter starts at one by default
    
    return areas



TEST_DATA_RAW = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

TEST_DATA = TEST_DATA_RAW.split("\n")  # list of strings
TEST_POINTS = [Point.from_line(line) for line in TEST_DATA]


test_nrst = get_nearests_grid(TEST_POINTS)
test_areas = calc_areas(test_nrst)
#print(test_areas)

# Unit tests:
assert test_areas[4] == 17
assert test_areas[3] == 9
assert len(test_areas) == 2



with open("data/day06.txt") as f:
    lines = [line.strip() for line in f]
    points = [Point.from_line(line) for line in lines]  # list of points
    

nrst = get_nearests_grid(points)
areas = calc_areas(nrst)

print(areas)
# What is the size of the largest area that isn't infinite?
# Answer is the first value: 3260


#########
# Part B:

#For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. 
#For each location, add up the distances to all of the given coordinates; 
#if the total of those distances is less than 32, that location is within the desired region. 

def calc_squares_within_dist(points: List[Point], total_dist_less_than: int) -> int:
    """
    go thru the extended grid of points. For each Point, get the total manhattan dist to all points
    if the total dist is below the "dist_less_than", accumulate the total area that will be returned
    """
    x_min = min(point.x for point in points)
    x_max = max(point.x for point in points)
    y_min = min(point.y for point in points)
    y_max = max(point.y for point in points)
    
    # extend the grid by "margin"... outside this extended grid cannot be any squares that fulfill the "total_dist_less_than" condition 
    margin = total_dist_less_than // len(points)
    
    num_squares_within = 0
    
    for x in range(x_min - margin, x_max + margin + 1):
        for y in range(y_min - margin, y_max + margin + 1):
            total_dist = Point(x, y).total_manhattan_distance(points)
            if total_dist < total_dist_less_than:
                num_squares_within += 1

    return num_squares_within
    

print("Squares within the given upper bound total manhattan dist:", calc_squares_within_dist(points, 10000))


