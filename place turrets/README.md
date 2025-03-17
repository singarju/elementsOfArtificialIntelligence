# a0-release
About the code:

It begins by parsing the map. It reads the maze file map and returns it as a 2D list. Once the parsing is done, the code checks for valid_index, that is, to check the file for the row,col pair.This ensures that the postion of (row,col) is within the bounds of the maze. Next, it tries to find the possible moves. This generates possible moves from the given position (row,col) and filters out all the invalid or blocked moves. The code can move in 4 directions, i.e., Up, Down, Left and Right. Once the code analyzes the map, it tries to search for a path to the goal. This particular algorithm uses Depth-first search to find the shortest path from 'p' to '@'. There are three main variables used in this algorithm. 
1) Fringe: Uses current_loc to update the current location of the state and push it inside a stack. 
2) Reached: To show the visited nodes and 
3) Parent: Track parents for path reconstruction. 
Once the goal is found, it converts it into a string of Directions (U,D,L,R). If no path is found, it returns -1 and an empty string.

Problems faced:

The reference code shared had an error and created an endless loop because the code keeps going back to the previously visited nodes. Thus creating a loop with same set of moves. To prevent this issue, we created a new function variable called "Reached". This makes sure that the code doesn't visit the same set of moves twice. 
