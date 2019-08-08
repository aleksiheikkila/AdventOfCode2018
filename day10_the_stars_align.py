"""
Advent of code, 2018
Day 10: The stars align
"""

import re
import numpy as np
from typing import List, Tuple

#Input format: position=<-31492,  42429> velocity=< 3, -4>
rgx = "position=<([- ]\d+), ([- ]\d+)> velocity=<([- ]\d+), ([- ]\d+)>"


# given enough time, those positions and velocities will move the points into a cohesive message!

# when cohesive?
# They move together. Then they start to drift apart.
# Probably when the bounding box of the points is the smallest! (Assumption is that all the points participate in forming the message)



class Point():
    """
    coordinates,
    velocity
    step() method to take one step, update location
    from_line static method to create
    """
    x: int
    y: int
    vx: int
    vy: int
    
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    
    def step(self, num_steps: int = 1):
        """
        take one step
        """
        self.x += num_steps*self.vx
        self.y += num_steps*self.vy
        
    @staticmethod
    def from_line(line: str) -> 'Point':
        """
        parses the line of input, returns corresponding point object
        """
        x,y,vx,vy = map(int, re.match(rgx, line).groups())   # re.match anchored to the start of the string... re.search not
        return Point(x,y,vx,vy)
 
 
class Sky():  
    def __init__(self, points: List[Point], time: int = 0):
        self.time = time
        self.points = points
        self.update_bounding_box()
        self.min_bb_area = self.bb_area
        
    
    def timestep(self, num_steps: int = 1):
        self.time += num_steps
        for point in self.points:
            point.step(num_steps)
        self.update_bounding_box()
        
    def draw(self, output_file: str = "adventofcode2018_day10_pic.txt") -> int:
        """
        return the time when the message appears        
        """
        x_range = self.bb_coords[2] - self.bb_coords[0] + 1
        y_range = self.bb_coords[3] - self.bb_coords[1] + 1
        print("Ranges:", x_range, y_range)
        
        self.pic = np.chararray((y_range, x_range), unicode=True)
        self.pic[:] = "."
        
        for point in self.points:
            self.pic[point.y - self.bb_coords[1], point.x - self.bb_coords[0]] = "#"
                
        with open(output_file, "w") as f:
            for row in self.pic:
                add_line = "".join(row.tolist()) + "\n"
                f.write(add_line)

        
        
        
    def update_bounding_box(self):
        min_x = min(point.x for point in self.points)
        min_y = min(point.y for point in self.points)
        max_x = max(point.x for point in self.points)
        max_y = max(point.y for point in self.points)
        
        self.bb_coords = (min_x, min_y, max_x, max_y)
        self.bb_area = (max_x - min_x + 1) * (max_y - min_y + 1)

   

# reformatted just slightly to match the actual input
INPUT_RAW = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6,  10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6,  10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3,  11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=< 10, -3> velocity=<-1,  1>
position=< 5,  11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=< 15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=< 14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""


INPUT_TEST = INPUT_RAW.split("\n")
print(INPUT_TEST)
points_test = [Point.from_line(line) for line in INPUT_TEST]
print(points_test)

sky_test = Sky(points_test, time=0)

while True:
    sky_test.draw(output_file = "adventofcode2018_day10_unittest_pic.txt")  # inefficient but okay with the unit test case
    sky_test.timestep()
    if sky_test.bb_area > sky_test.min_bb_area:  # starts to drift apart
        print("Finished")
        break
    else:
        sky_test.min_bb_area = sky_test.bb_area



with open("data/day10.txt") as f:
    input = [line.strip() for line in f]
    
points = [Point.from_line(line) for line in input]

sky = Sky(points, time=0)

# Now the larger one: do not draw before we are at the minimum bbox
while True:
    sky.timestep()
    if sky.bb_area > sky.min_bb_area:
        print("Finished")
        sky.timestep(-1)
        sky.draw()
        print("Timestep when the msg appeared:", sky.time)
        break
    else:
        sky.min_bb_area = sky.bb_area

# Your puzzle answer was NBHEZHCJ.

# Part B:
# timestep when the msg appeared
# Answer: 10558