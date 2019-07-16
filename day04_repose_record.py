"""
Advent of code, 2018
Day 4: Repose record
"""

from collections import Counter
import re

rgx = "Guard #([0-9]+) begins shift"

# format is like:
# [1518-05-09 00:01] Guard #743 begins shift

with open("data/day04.txt") as f:
    log = [line.strip() for line in f]

# sort to chonol. order
log.sort()


# Better structure: Sleep as a class...


def total_sleep_times(log):
    """
    returns:
        dict (guard id as a key) of total_sleep_times per guard id
        dict (guard id as a key) of sums of guard's sleep times for each minute in a Counter
    """
    
    sleep_times = dict()   # guard id is the key, Counter is the value with starting minute
    total_sleep_times = Counter()
    
    guard = None
    
    for entry in log:
        match = re.search(rgx, entry)   # new guard begins shift...
        
        if match:
            guard = int(match.groups()[0])
            if guard not in sleep_times:
                sleep_times[guard] = Counter()
                
            fell_asleep_time = None
            woke_up_time = None
            continue
        
        if "falls asleep" in entry:
            fell_asleep_time = entry.split(":")[1][:2]   # as str
            continue
            
        if "wakes up" in entry:
            woke_up_time = entry.split(":")[1][:2]
            
            # check that the case seems valid
            if all((guard, fell_asleep_time, woke_up_time)):
                duration_sleep = int(woke_up_time) - int(fell_asleep_time)
                
                total_sleep_times[guard] += duration_sleep
                
                for minute in range(int(fell_asleep_time), int(woke_up_time)):
                    sleep_times[guard][minute] += 1
                
                fell_asleep_time = None
                woke_up_time = None
                
            else:
                raise Exception("Not all data found")


    return total_sleep_times, sleep_times      

    
sleepsums, sleeptimes = total_sleep_times(log)


most_sleepy_guard_id = sleepsums.most_common(1)[0][0]

most_often_slept_minute = sleeptimes[most_sleepy_guard_id].most_common(1)[0][0]
# Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

print(most_sleepy_guard_id, most_often_slept_minute, most_sleepy_guard_id * most_often_slept_minute)

# What is the ID of the guard you chose multiplied by the minute you chose?


# Unit test:
TEST_LOG = [
    "[1518-11-01 00:00] Guard #10 begins shift",
    "[1518-11-01 00:05] falls asleep",
    "[1518-11-01 00:25] wakes up",
    "[1518-11-01 00:30] falls asleep",
    "[1518-11-01 00:55] wakes up",
    "[1518-11-01 23:58] Guard #99 begins shift",
    "[1518-11-02 00:40] falls asleep",
    "[1518-11-02 00:50] wakes up",
    "[1518-11-03 00:05] Guard #10 begins shift",
    "[1518-11-03 00:24] falls asleep",
    "[1518-11-03 00:29] wakes up",
    "[1518-11-04 00:02] Guard #99 begins shift",
    "[1518-11-04 00:36] falls asleep",
    "[1518-11-04 00:46] wakes up",
    "[1518-11-05 00:03] Guard #99 begins shift",
    "[1518-11-05 00:45] falls asleep",
    "[1518-11-05 00:55] wakes up"
]

test_sleepsums, test_sleeptimes = total_sleep_times(TEST_LOG)

assert test_sleepsums.most_common(1)[0][0] == 10
assert test_sleepsums.most_common(1)[0][1] == 50
assert test_sleepsums[99] == 30
assert test_sleeptimes[10].most_common(1)[0][0] == 24

#Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), 
#while Guard #99 only slept for a total of 30 minutes (10+10+10). 
#Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

print(sleeptimes)

# Part 2:
# Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

# What is the ID of the guard you chose multiplied by the minute you chose?

def most_freq_same_min_napper(log):
    _, sleep_times = total_sleep_times(log)
    
    target_guard = most_freq_minute = None
    max_naps = -1
    
    for guard, nap_stats in sleep_times.items():
        if len(nap_stats) == 0:
            continue
        
        print(nap_stats.most_common(1))
        top_naps = nap_stats.most_common(1)[0][1]
        
        if (top_naps > max_naps):
            max_naps = top_naps
            most_freq_minute = nap_stats.most_common(1)[0][0]
            target_guard = guard
        
    return target_guard, most_freq_minute, top_naps, target_guard * most_freq_minute

    
    
print(most_freq_same_min_napper(log))
