#!/usr/local/bin/python3
#
# mystical_castle.py : a maze solver
#
# Submitted by : vvaradh-yuhirata-singarju
#
# Based on skeleton code provided in CSCI B551, Fall 2024.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the castle_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the castle map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(castle_map):
        # Find current start position
        current_loc=[(row_i,col_i) for col_i in range(len(castle_map[0])) for row_i in range(len(castle_map)) if castle_map[row_i][col_i]=="p"][0]
        start_loc = current_loc

        fringe=[(current_loc,0)]

        reached = [[False for i in range(len(castle_map[0]))] for j in range(len(castle_map))]
        parent = [[(0,0) for i in range(len(castle_map[0]))] for j in range(len(castle_map))]

        while fringe:
                # First location marked as reached
                reached[current_loc[0]][current_loc[1]] = True

                (curr_move, curr_dist)=fringe.pop()
                # Find possible moves from current location
                for move in moves(castle_map, *curr_move):
                        if castle_map[move[0]][move[1]]=="@":
                                reached[move[0]][move[1]] = True
                                fringe.append((move, curr_dist + 1))
                                parent[move[0]][move[1]] = curr_move
                                current_loc = move
                                path = [0 for i in range(curr_dist + 2)]
                                loc = move
                                num = 0
                                while loc != start_loc:
                                    path[num] = loc
                                    loc = parent[loc[0]][loc[1]]
                                    num += 1
                                path[num] = start_loc
                                path.reverse()
                                entire_path = []
                                for i in range(1, len(path)):
                                    if path[i][0] - path[i-1][0] == 1:
                                        entire_path.append("D")
                                    elif path[i][0] - path[i-1][0] == -1:
                                        entire_path.append("U")
                                    elif path[i][1] - path[i-1][1] == 1:
                                        entire_path.append("R")
                                    elif path[i][1] - path[i-1][1] == -1:
                                        entire_path.append("L")
                                return(curr_dist + 1, "".join(entire_path))
                        else:
                                # Depth-first search
                                if reached[move[0]][move[1]] == False:
                                        reached[move[0]][move[1]] = True
                                        fringe.append((move, curr_dist + 1))
                                        parent[move[0]][move[1]] = curr_move
                                        current_loc = move
        # If there is no solution, display path length -1 and not display a path.
        return -1, ""

# Main Function
if __name__ == "__main__":
        castle_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(castle_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

