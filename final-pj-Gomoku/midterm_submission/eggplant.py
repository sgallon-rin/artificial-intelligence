'''
AI final project Gomoku

Name: Jialun Shen
Sid: 16307110030
Name: Jinming Liu
Sid: 17307110101
'''

import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy

pp.infotext = 'name="pbrain-eggplant", author="Jialun Shen, Jinming Liu", version="1.0", country="China"'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

# given a position, and the distance around the position, return the possible continue positions
def getline(position,distance): # poisiton is like (x,y), distance is the distance between position and positive available position
    x,y=position
    result=[] # it will return as [[[x1,y1],[x2,y2]...],[...],...], 8 directions in total
    if (x+distance)>=0 and (x+distance)<20:
        result1 = []
        for i in range(distance):
            result1.append([x + i + 1, y])
        result.append(result1)
    if (x+distance)>=0 and (x+distance)<20 and (y+distance)>=0 and (y+distance)<20: # to satisfy that the size is ok
        result2 = []
        for i in range(distance):
            result2.append([x + i + 1, y + i + 1])
        result.append(result2)
    if (y+distance)>=0 and (y+distance)<20:
        result3 = []
        for i in range(distance):
            result3.append([x, y + i + 1])
        result.append(result3)
    if (x-distance)>=0 and (x-distance)<20 and (y+distance)>=0 and (y+distance)<20:
        result4 = []
        for i in range(distance):
            result4.append([x - i - 1, y + i + 1])
        result.append(result4)
    if (x-distance)>=0 and (x-distance)<20:
        result5 = []
        for i in range(distance):
            result5.append([x - i - 1, y])
        result.append(result5)
    if (x-distance)>=0 and (x-distance)<20 and (y-distance)>=0 and (y-distance)<20:
        result6 = []
        for i in range(distance):
            result6.append([x - i - 1, y - i - 1])
        result.append(result6)
    if (y-distance)>=0 and (y-distance)<20:
        result7 = []
        for i in range(distance):
            result7.append([x, y - i - 1])
        result.append(result7)
    if (x+distance)>=0 and (x+distance)<20 and (y-distance)>=0 and (y-distance)<20:
        result8 = []
        for i in range(distance):
            result8.append([x + i + 1, y - i - 1])
        result.append(result8)
    return result

# given board, a position on board which is empty now, return a value to evaluate how good the position is
def evaluate(board,position,player):
    if player == 1: # if player is 1, means that my turn
        me = 1
        oppo = 2
    if player == 2: # if player is 2, means that opposite's turn
        me = 2
        oppo = 1
    values = [0]
    
    for i in getline(position, 5): # if 5 together before, the game was over, return 0 as reward
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != me: 
                caps = 1
        if caps == 0:
            return 0
    caps = 0
    for i in getline(position, 5): #  if 5 together before, the game was over, return 0 as reward
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != oppo:
                caps = 1
        if caps == 0:
            return 0
    caps = 0
    for i in getline(position,4):# 5 together, I win, take 10^4 as reward
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != me:
                caps=1
        if caps==0:
            values.append(10000)
            break
    caps = 0
    for i in getline(position,4):# if opposite already has 4 together, have to avoid 5.take 0.9*10^4. and the case below is similar.
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != oppo:
                caps=1
        if caps==0:
            values.append(9000)
            break
    caps = 0
    for i in getline(position, 3):
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != me:
                caps = 1
        if caps == 0:
            values.append(1000)
            break
    caps = 0
    for i in getline(position, 3):
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != oppo:
                caps = 1
        if caps == 0:
            values.append(900)
            break
    caps = 0
    for i in getline(position, 2):
        caps = 0
        for j in i:
            if board[j[0]][j[1]]!= me:
                caps = 1
        if caps == 0:
            values.append(100)
            break
    caps = 0
    for i in getline(position, 2):
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != oppo:
                caps = 1
        if caps == 0:
            values.append(90)
            break
    caps = 0
    for i in getline(position, 1):
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != me:
                caps = 1
        if caps == 0:
            values.append(10)
            break
    caps = 0
    for i in getline(position, 1):
        caps = 0
        for j in i:
            if board[j[0]][j[1]] != oppo:
                caps = 1
        if caps == 0:
            values.append(9)
            break
    return max(values)

class Node: # definite a class as node, has value and successor
    def __init__(self,  successor=None,  value=None):
        if successor is None:
            successor = []
        self.successor = successor
        self.value = value

def construct_tree(state): # construct a tree ,though it has only one level, but next function "find_position_by_alpha_bata" will make it function as two levels tree!
    node = Node(value=state)
    positions = get_son_position(state)
    successors = []
    for i in positions:
        state_temp = copy.deepcopy(state)
        state_temp[i[0]][i[1]] = 1
        successors.append(Node(value=state_temp))
    node.successor=successors
    return node


def find_position_by_alpha_beta(node): # input root node of a tree, it will firstly make one level tree function as 2 level tree, and secondly use alpha beta cut to achieve mini_max function
    if len(node.successor) == 1:
        return get_son_position(node.value)[0]
    else:
        node_positions = get_son_position(node.value)
        beta = float("-inf")
        target_index = 0
        for k in node.successor:
            positions = get_son_position(k.value)
            minimize = float("inf")
            for i in positions:
                leaf_value = evaluate(node.value,node_positions[node.successor.index(k)],player=1)-0.1*evaluate(k.value,i,player=2) # leaf value, evaluate target. gamma=0.1
                if leaf_value < beta:
                    break
                if leaf_value < minimize:
                    minimize = leaf_value
            if minimize > beta and minimize != float("inf"):
                beta = minimize
                target_index = node.successor.index(k)
        return node_positions[target_index]

def get_son_position(state): # given a board, return all posible free position the next step can be.
    positions = []
    caps = 0
    for x in range(20):
        for y in range(20):
            if state[x][y] != 0:
                caps = 1
                for i in range(5):
                    for j in range(5):
                        if isFree(x+i-2, y+j-2) and [x+i-2, y+j-2] not in positions:
                            positions.append([x+i-2, y+j-2])
    if caps == 0:
        positions.append([10,10])
    return positions

def brain_init():
	if pp.width < 5 or pp.height < 5:
		pp.pipeOut("ERROR size of the board")
		return
	if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
		pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
		return
	pp.pipeOut("OK")

def brain_restart():
	for x in range(pp.width):
		for y in range(pp.height):
			board[x][y] = 0
	pp.pipeOut("OK")

def isFree(x, y):
	return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def brain_my(x, y):
	if isFree(x,y):
		board[x][y] = 1
	else:
		pp.pipeOut("ERROR my move [{},{}]".format(x, y))

def brain_opponents(x, y):
	if isFree(x,y):
		board[x][y] = 2
	else:
		pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))

def brain_block(x, y):
	if isFree(x,y):
		board[x][y] = 3
	else:
		pp.pipeOut("ERROR winning move [{},{}]".format(x, y))

def brain_takeback(x, y):
	if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
		board[x][y] = 0
		return 0
	return 2

def brain_turn():
	if pp.terminateAI:
		return
	i = 0
	while True:
		x, y = find_position_by_alpha_beta(construct_tree(board))
		i += 1
		if pp.terminateAI:
			return
		if isFree(x,y):
			break
	if i > 1:
		pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
	pp.do_mymove(x, y)

def brain_end():
	pass

def brain_about():
	pp.pipeOut(pp.infotext)

if DEBUG_EVAL:
	import win32gui
	def brain_eval(x, y):
		# TODO check if it works as expected
		wnd = win32gui.GetForegroundWindow()
		dc = win32gui.GetDC(wnd)
		rc = win32gui.GetClientRect(wnd)
		c = str(board[x][y])
		win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
		win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "/tmp/pbrain-pyrandom.log"
# ...and clear it initially
with open(DEBUG_LOGFILE,"w") as f:
	pass

# define a function for writing messages to the file
def logDebug(msg):
	with open(DEBUG_LOGFILE,"a") as f:
		f.write(msg+"\n")
		f.flush()

# define a function to get exception traceback
def logTraceBack():
	import traceback
	with open(DEBUG_LOGFILE,"a") as f:
		traceback.print_exc(file=f)
		f.flush()
	raise

# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
def brain_turn():
	logDebug("some message 1")
	try:
		logDebug("some message 2")
		1. / 0. # some code raising an exception
		logDebug("some message 3") # not logged, as it is after error
	except:
		logTraceBack()
"""
######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
	pp.brain_eval = brain_eval

def main():
	pp.main()

if __name__ == "__main__":
	main()
