#importing student's scripts
import mystical_castle
from itertools import groupby
import pandas as pd
import re
import os
import pytest

def navigate(mapX,moves):
	# Find my start position
	you_loc=[(row_i,col_i) for col_i in range(len(mapX[0])) for row_i in range(len(mapX)) if mapX[row_i][col_i]=="p"][0]
	# Find goal location
	goal_loc=[(row_i,col_i) for col_i in range(len(mapX[0])) for row_i in range(len(mapX)) if mapX[row_i][col_i]=="@"][0]    
	moves=moves.lower()
	try:
		you_row,you_col=you_loc
		for i,move in enumerate(moves):
			if move=='u':
				#moving up only row dimension (index position 0 of you_loc) updated
				you_row-=1
			elif move=='d':
				#moving down only row dimension (index position 0 of you_loc) updated
				you_row+=1
			elif move=='r':
				#moving right only col dimension (index position 1 of you_loc) updated
				you_col+=1
			elif move=='l':
				#moving left only col dimension (index position 1 of you_loc) updated
				you_col-=1
			if i == len(moves)-1:
				#True if Provided Path reaches the Goal
				return mapX[you_row][you_col]=='@'
			elif mapX[you_row][you_col]=='X':
				#Return False if Provided Path contains invalid moves
				return False
	except IndexError:
		#Moves go off the map
		return False

#Part 1 needs to return the int:dist, str_list:moves
def check_solution1(mapX,dist_key):
	regex_moves=re.compile(r'^[UDRLudrl]+$')
	#function to search
	dist,moves=mystical_castle.search(mapX)
	assert type(dist)==int,"Distance is not an integer"
	assert dist==dist_key,"Wrong solution"
	if dist>-1:
		assert regex_moves.match(moves),"Moves contain invalid characters"
		assert dist==len(moves),"Distance and path length are not equal"
		assert navigate(mapX,moves)==True,"Path did not reach the goal"


def load_maps():
	maps=[]
	for name in ['map1.txt','map2.txt']:
		with open(name,"r") as file:
			lines=file.read().splitlines()
			dist=int(lines[0])
			sol_exist=bool(lines[1]) # ignore this for now
			n=int(lines[2]) # ignore this for now
			mapX=[list(line) for line in lines[3:]]
			maps.append((mapX,dist,sol_exist,n))
	return maps

time_ = 300
@pytest.mark.timeout(time_)
def test_question1_case1():
	maps=load_maps()
	mapX,dist_key,_,_=maps[0]
	check_solution1(mapX,dist_key)

@pytest.mark.timeout(time_)
def test_question1_case2():
	maps=load_maps()
	mapX,dist_key,_,_=maps[1]
	check_solution1(mapX,dist_key)