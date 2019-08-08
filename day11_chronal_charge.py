"""
Advent of code, 2018
Day 11: Chronal Charge
"""

from typing import Tuple, Dict
import numpy as np

GRID_SERIAL_NUM = 7989  # puzzle input


def get_power_level(x:int, y:int, grid_serial_num:int) -> int:
    """
    given coordinates, return the power level
    """
    rack_id = x + 10
    power = rack_id * y
    power += grid_serial_num
    power *= rack_id
    power = 0 if power < 100 else int(str(power // 100)[-1])
    power -= 5
    
    return power
    
# unit tests for power level calculation
assert get_power_level(122, 79, 57) == -5
assert get_power_level(217, 196, 39) == 0
assert get_power_level(101, 153, 71) == 4



def get_cell_powers(grid_serial_num:int, x_max: int = 300, y_max: int = 300) -> "np.ndarray[int]":
    """
    returns numpy array with the cell powers.
    Indexing starts from zero in np.array. Index [0,0] contains the point [1,1] as described in the problem.
    """
    cell_powers = np.zeros((x_max, y_max))
    for x in range(x_max):
        for y in range(y_max):
            cell_powers[x,y] = get_power_level(x+1, y+1, grid_serial_num)  # fix zero one indexing mismatch. Now index 0 corresponds to 1 in the problem statement
    
    return cell_powers
    

def find_max_power_square(cell_powers: "np.ndarray[int]", square_size: int = 3) -> Tuple[Tuple[int, int], int]:
    """
    find the square_size x square_size square that has the maximal sum of cell powers
    Returns its index as a tuple, with the actual max value
    """
    x_max, y_max = cell_powers.shape
    square_powers = {}
    
    for x in range(0, x_max + 1 - square_size):   
        for y in range(0, y_max + 1 - square_size):
            square_sum = sum(sum(cell_powers[x:x+square_size, y:y+square_size]))
            square_powers[(x+1, y+1)] = int(square_sum)
    
    #return square_powers
    max_key = max(square_powers, key=square_powers.get)
    max_val = square_powers[max_key]
    
    return max_key, max_val


def find_max_total_power_square(cell_powers: "np.ndarray[int]") -> Tuple[Tuple[int, int, int], int]:
    """
    
    """
    total_powers = {}
    
    x_max, y_max = cell_powers.shape
    
    for square_size in range(1, x_max+1):
        print(f"Analysing square size of {square_size}")
        (x, y), max_val = find_max_power_square(cell_powers=cell_powers,
                                                square_size = square_size)
                                     
        total_powers[(x,y,square_size)] = max_val
        
    max_key = max(total_powers, key=total_powers.get)
    max_val = total_powers[max_key]
    
    return max_key, max_val
    


# Unit tests
assert find_max_power_square(cell_powers=get_cell_powers(grid_serial_num=18))[0] == (33, 45)
assert find_max_power_square(cell_powers=get_cell_powers(grid_serial_num=42))[0] == (21, 61)


# With own input:
cell_powers = get_cell_powers(grid_serial_num = GRID_SERIAL_NUM)
print(find_max_power_square(cell_powers=cell_powers))
# 19,17 is the answer


# Part B:
# Okay, the issue now it the performance of the algorithm.
total_powers = find_max_total_power_square(cell_powers = cell_powers)
print(total_powers)
# The answer is: 233,288,12


