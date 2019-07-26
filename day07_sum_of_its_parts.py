"""
Advent of code, 2018
Day 7: The Sum of Its Parts
"""

import re

from collections import defaultdict
from typing import Tuple, Set, Dict, List, NamedTuple
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

def step_duration(step: str, base: int = 60) -> int:
    return base + ord(step) - ord("A") + 1

assert step_duration("A") == 61
assert step_duration("Z") == 86
assert step_duration("D", 0) == 4

# Part B to be refactored...

class WorkItem(NamedTuple):
    """
    just a "data type" for workitems
    """
    item_name: str
    worker_id: int
    start_time: int
    end_time: int
    

def find_time_to_complete(requirements: List[Req], num_workers: int, base: int = 60) -> int:
    """
    returns the total time required for completing all the steps
    """
    prereqs = get_prerequirements(requirements)
    
    #workers = {id for id in range(num_workers)}
    active_work = [None for _ in range(num_workers)]   # one slot for each worker
    
    time = 0
    
    # Loop until all steps are finished
    while prereqs or any(active_work):  # the latter part of the condition: in the end, take care that we track the situation until the very end
        # Check if someone finished:
        for idx, work_item in enumerate(active_work):
            if work_item and work_item.end_time <= time:  # guard agains NoneType as work_item (in the beginning)
                active_work[idx] = None
               
               # then update the prereqs by removing the finished step from the requirements (this is no longer constraining as its done...)
                for reqs in prereqs.values():
                    if work_item.item_name in reqs:
                        reqs.remove(work_item.item_name)
                
        
        # get available workers
        available_workers = [i for i in range(num_workers) if active_work[i] is None]
        
        # Allowed steps
        allowed_steps = [step for step, reqs in prereqs.items() if not reqs]   #  empty sequences are false.
        allowed_steps.sort()      
        

        # Allocate allowed steps to workers (as many as possible)
        for worker_id, step in zip(available_workers, allowed_steps):  # shorter
            active_work[worker_id] = WorkItem(step, worker_id, time, time + step_duration(step, base))
            del prereqs[step]
        
        
        # nothing happens until the min of WorkItem end_times. Fast-forward there:
        if any(active_work):
            time = min(work_item.end_time for work_item in active_work if work_item)  # guard against NoneType in the end

    return time

# unit test:
assert find_time_to_complete(TEST_REQS, num_workers=2, base=0) == 15

print(find_time_to_complete(reqs, num_workers=5))
# 880 is the right answer.