"""
Advent of code, 2018
Day 7: The Sum of Its Parts
"""

import re

from collections import defaultdict
from typing import Tuple, Set, Dict, List
from copy import copy, deepcopy

# regex for parsing the input lines
rgx = "Step (\w) must be finished before step (\w) can begin."

# Requirement. A tuple of before - after, i.e. "must be finished before", "can be done then"
Req = Tuple[str, str]

# All (immediate) prerequisites for a step (= dict keys)
Prereqs = Dict[str, Set[str]]

# Part A:
# The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). 
# Each step is designated by a single letter. For example, suppose you have the following instructions:

# Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically.


def req_from_line(line: str) -> Req:
    """
    given line of the raw input data, returns Tuple of before - after step pairs as strings
    """
    before, after = re.match(rgx, line).groups()
    return (before, after)
        
def get_prerequirements(requirements: List[Req]) -> Prereqs:
    """
    returns a Dict where we have every step as a key. Its value is a set of immediate prerequirements that must be finished before the step can begin
    """
    all_steps = {step for req in requirements for step in req}
    
    # initialize
    prereqs = {step: set() for step in all_steps}

    # add actual requirements
    for pre, post in requirements:
        prereqs[post].add(pre)
    
    return prereqs


def find_step_order(requirements: List[Req]) -> str:
    """
    
    """
    
    order = []
    
    prereqs = get_prerequirements(requirements)
    
    while prereqs:
        allowed_steps = [step for step, reqs in prereqs.items() if not reqs]   #  empty sequences are false.
        next_step = min(allowed_steps)
        
        order.append(next_step)
        del prereqs[next_step]
        
        # then update the prereqs by removing next_step from the requirements (this is no longer constraining as its done...)
        for reqs in prereqs.values():
            if next_step in reqs:
                reqs.remove(next_step)
            
    # while finishes after all steps are picked
    return "".join(order)
        

    
TEST_DATA_RAW = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

TEST_DATA = TEST_DATA_RAW.split("\n")

TEST_REQS = [req_from_line(line) for line in TEST_DATA]
print(TEST_REQS)
assert TEST_REQS[2] == ("A", "B")

TEST_PREREQS = get_prerequirements(TEST_REQS)
print(TEST_PREREQS)
assert TEST_PREREQS["C"] == set()
assert TEST_PREREQS["E"] == {"B", "D", "F"}

TEST_ORDER = find_step_order(TEST_REQS)
print(TEST_ORDER)
assert TEST_ORDER == "CABDFE"


# With the problem data: In what order should the steps in your instructions be completed?
with open("data/day07.txt") as f:
    lines = [line.strip() for line in f]

reqs = [req_from_line(line) for line in lines]

order = find_step_order(reqs)
print(order)


    
# Part B:
# can work in parallel
# Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on

# With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?

def step_duration(step: str) -> int:
    return 60 + ord(step) - ord("A") + 1

assert step_duration("A") == 61
assert step_duration("Z") == 86

# Part B to be refactored...

def find_time_to_complete(requirements: List[Req], num_workers: int) -> int:
    pass

# 880 right answer.
