# singarju-a1

# a1-release
The first thing that comes to mind after reading the question is the n-queen problem, but here we neither have nXn matrics nor n queens. Instead we have a  matrix of size aXb and we need to place m queen in entire map. The  problem is similar to the n-queen problem but with some modifications. I can solve this problem by
1) Initialize the fringe with the initial state
2) Run a loop for row and a nested loop for column to access the elements of the map
3) Write another function which can check if we can place turrents at a given index or not
    - check for the row and column and diagonals
4) if we can place a turret we add the turret and push it to the new map and increment the value of number of turrets placed till now
5) Call the solve function again  with the new map and the number of turrets placed till now.
6) If we've placed k-1 turrets, return the current state and True. (k-1 because one turret is already fixed in the initial map)
7) If we can't fit all the turrets, return false
