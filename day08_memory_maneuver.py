"""
Advent of code, 2018
Day 8: Memory Maneuver
"""

from typing import List


class Node():
    """
    Node class slightly tailored for the purpose of this problem
    """
    def __init__(self, num_childs: int, num_metadata: int,  children: List["Node"], parent: "Node" = None):
    
        self.num_childs = num_childs
        self.num_metadata = num_metadata
        
        self.parent = parent
        
        self.children = []
        if children:
            for child in children:
                self.children.append(child)
        
        self.metadata = []
        
        # this keeps track how many of Nodes children has been processed (by find nodes' sort of depth first search)
        self.num_child_processed = 0
        
        # for part B, the value of the node
        self.value = 0
        
    def __str__(self):
        """
        object representation, just for simple debugging
        """
        return "NODE: " + str(self.num_childs) + " " + str(self.num_metadata)
        

TEST_DATA_RAW = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
TEST_DATA = TEST_DATA_RAW.split(" ")


def find_nodes(input_line: str) -> List[Node]:
    """
    returns found Nodes in a list.
    uses global variable "root" for the root node
    """
    li = [int(elem) for elem in input_line.split(" ")]
    assert len(li) >= 2
    
    # store Nodes in two sets, depending is their processing ready or not
    unfinished = set()
    finished = set()
    
    
    i = 0   # points to the index where to read the input list
    parent = None
    
    # add root node
    global root   # global so we can directly grab its value outside this func
    root = Node(num_childs = li[i], num_metadata = li[i+1], children = None,  parent = parent)
    print("Added root node:", root)
    
    # Logic for handling the root node
    if root.num_childs > 0:
        unfinished.add(root)  # assumes more to come...
        i += 2   # continue from child's first element
    else:  # root node does not have children
        finished.add(root)
        i += 2 + num_metadata
        
    parent = root
    
    
    all_done = False   # set to True when all nodes has been processed (to break out of the loop)
    
    # now we have a root ready
    while i < len(li):
        #print(i)
                
        while parent.num_child_processed >= parent.num_childs:
            # backtrack a step towards root node!
            # store metadata elements
            parent.metadata = li[i: i+parent.num_metadata]
            
            # calculate node value
            parent.value = sum(parent.children[idx - 1].value for idx in parent.metadata if idx > 0 and idx <= parent.num_childs)
            
            finished.add(parent)
            unfinished.remove(parent)
            i += parent.num_metadata
            
            if parent.parent:
                parent = parent.parent
            else:  # was root
                print("Backtracking out from root, hence all done")
                all_done = True
                break
        
        if all_done:
            break
        
        curr_num_childs, curr_num_metadata = li[i], li[i+1]
        
        # create a new node
        curr_node = Node(num_childs = curr_num_childs, num_metadata = curr_num_metadata, children = None, parent = parent)
        #print("Found new node:", curr_num_childs, curr_num_metadata, "\t\tparent:", parent)
        parent.children.append(curr_node)
        parent.num_child_processed += 1
        
        if curr_num_childs > 0:  # current node has children
            unfinished.add(curr_node)
            i = i + 2   # continue with the child
            parent = curr_node  # which has current node as its parent
        else:   # current node is a leaf node
            curr_node.metadata = li[i+2: i+2+curr_num_metadata]
            # calculate node value
            curr_node.value = sum(curr_node.metadata)
            
            finished.add(curr_node)
            i = i + 2 + curr_num_metadata
    
    return finished


finished_nodes = find_nodes(TEST_DATA_RAW)
sum_metadatas = sum(metadata for node in finished_nodes for metadata in node.metadata)
print("sum of metadata entries:", sum_metadatas)

# unit test:
assert sum_metadatas == 138



# Now with the  full input data
# Part A
# What is the sum of all metadata entries?
with open("data/day08.txt") as f:
    input = f.read().strip()

nodes = find_nodes(input)
sum_meta = sum(metadata for node in nodes for metadata in node.metadata)
print(sum_meta)
# Answer is: 44893


#################
# Part B

# added calculation of the value in the function above,
# starting from the leaf nodes, building toward the root
# plus made root node global, so we can just get its value here by:
print(root.value)
# 27433
