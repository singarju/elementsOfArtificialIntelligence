#!/usr/local/bin/python3
#
# place_turrets.py : arrange turrets on a map_grid, avoiding conflicts
#
# Submitted by : [Arju Singh(singarju)]
#
# Based on skeleton code in CSCI B551, Fall 2024.
 
import sys
 
# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
 
# Count total # of turrets on castle_map
def count_turrets(castle_map):
    return sum([ row.count('p') for row in castle_map ] )
 
# Return a string with the castle_map rendered in a human-turretly format
def printable_castle_map(castle_map):
    return "\n".join(["".join(row) for row in castle_map])
 
# Add a turret to the castle_map at the given position, and return a new castle_map (doesn't change original)
def add_turret(castle_map, row, col):
    return castle_map[0:row] + [castle_map[row][0:col] + ['p',] + castle_map[row][col+1:]] + castle_map[row+1:]
 
# Get list of successors of given castle_map state
def successors(castle_map):
    return [ add_turret(castle_map, r, c) for r in range(0, len(castle_map)) for c in range(0,len(castle_map[0])) if castle_map[r][c] == '.' ]
 
# check if castle_map is a goal state
def is_goal(castle_map, k):
    return count_turrets(castle_map) == k
 
# Arrange turrets on the map
#
# This function MUST take two parameters as input -- the castle map and the value k --
# and return a tuple of the form (new_castle_map, success), where:
# - new_castle_map is a new version of the map with k turrets,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_castle_map, k):
    if k <= 1:
        return (initial_castle_map, True)
 
    fringe = [(initial_castle_map, 0)]  # Start with initial map and 0 turrets placed
 
    while len(fringe) > 0:
        current_map, current_count = fringe.pop()
 
        if current_count == k - 1:
            return (current_map, True)
 
        for r in range(len(current_map)):
            for c in range(len(current_map[0])):
                if current_map[r][c] == '.':
                    if can_place_turret(current_map, r, c):
                        new_castle_map = add_turret(current_map, r, c)
                        fringe.append((new_castle_map, current_count + 1))
 
    return (initial_castle_map, False)
 
def can_place_turret(map_grid, row, col):
    n = len(map_grid)  
    m = len(map_grid[0])  
 
    for c in range(col-1, -1, -1): 
        if map_grid[row][c] == 'X': 
            break
        if map_grid[row][c] == 'p': 
            return False
    for c in range(col+1, m): 
        if map_grid[row][c] == 'X': 
            break
        if map_grid[row][c] == 'p':
            return False
 
   
    for r in range(row-1, -1, -1):  
        if map_grid[r][col] == 'X':  
            break
        if map_grid[r][col] == 'p':  
            return False
    for r in range(row+1, n): 
        if map_grid[r][col] == 'X': 
            break
        if map_grid[r][col] == 'p': 
            return False
 
    
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if map_grid[r][c] == 'X': 
            break
        if map_grid[r][c] == 'p':
            return False
        r -= 1
        c -= 1
 
    r, c = row + 1, col + 1
    while r < n and c < m:
        if map_grid[r][c] == 'X': 
            break
        if map_grid[r][c] == 'p': 
            return False
        r += 1
        c += 1
 
    
    r, c = row - 1, col + 1
    while r >= 0 and c < m:
        if map_grid[r][c] == 'X': 
            break
        if map_grid[r][c] == 'p': 
            return False
        r -= 1
        c += 1
 
    r, c = row + 1, col - 1
    while r < n and c >= 0:
        if map_grid[r][c] == 'X':
            break
        if map_grid[r][c] == 'p':  
            return False
        r += 1
        c -= 1
 
    return True
 
# Main Function
if __name__ == "__main__":
    castle_map = parse_map(sys.argv[1])
    k = int(sys.argv[2])
    print("Starting from initial castle map:\n" + printable_castle_map(castle_map) + "\n\nLooking for solution...\n")
    solution = solve(castle_map, k)
    print("Here's what we found:")
    print(printable_castle_map(solution[0]) if solution[1] else "False")