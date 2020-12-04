'''
utils for Gomoku, evaluation function
Name: Jialun Shen
Sid: 16307110030
'''

# indicator for player
EMPTY = 0
ME = 1
OPP = 2
OUT = -1


def getline(position, direction, d, board, width, height):
    """
    给定一个点、一个方向、一个相对坐标值d，就能得到一个二维坐标，
    对应棋盘上一个点，返回该点的落子情况

    Input:
    position: (x,y)
    direction: int from 0 to 7, indicate a direction (p is position)
      x - >
    y 0 1 2
    | 3 p 4
    v 5 6 7
    d: distance between our point of interest and position
    board: a board
    width: upper bound for x
    height: upper bound for y

    Output:
    state of point of interest on board, i.e., 0/1/2
    returns -1 if out of range
    """
    x, y = position
    if direction == 0:
        x -= d
        y -= d
    elif direction == 1:
        y -= d
    elif direction == 2:
        x += d
        y -= d
    elif direction == 3:
        x -= d
    elif direction == 4:
        x += d
    elif direction == 5:
        x -= d
        y += d
    elif direction == 6:
        y += d
    elif direction == 7:
        x += d
        y += d
    else:
        print("ERROR Invalid direction, must be int 0-7")
        return
    
    if x < 0 or y < 0 or x >= width or y >= height:
        # print("ERROR Out of board, board size is {}{}".format(width, height))
        return OUT

    return board[x][y]


# values for different patterns
"""
Notations:
    * is the current position(should be empty)
    0 is empty
    1 is me
    # is opp or out
    $ is opp or out or empty
    & is me or out or empty
    ? is unknown

Value table:
name    |   pattern  |  value
open 4      01111*      300000
dead 4A     #1111*      250000
dead 4B     111*1       240000
dead 4C     11*11       230000
open 3A     0111*0      4000
open 3B     0111*#      500
open 3C     1110*       350
dead 3A     #111*0      750
dead 3B     011*10      3750
dead 3C     #11*1#      600
dead 3D1    #11*10      1300
dead 3D2    011*1#      1300
open 2 >=2  &11*& >=2   3000
"""
valueTable = {
    'OPEN4': 300000,
    'DEAD4_A': 250000,
    'DEAD4_B': 240000,
    'DEAD4_C': 230000,
    'OPEN3_A': 4000,
    'OPEN3_B': 500,
    'OPEN3_C': 350,
    'DEAD3_A': 750,
    'DEAD3_B': 3750,
    'DEAD3_C': 600,
    'DEAD3_D': 1300,
    'MULTI_OPEN2': 3000
}


def old_evaluate(position, board, width, height, ai=True):
    """
    evaluate the board if player put next piece at position(x,y)
    player is ai if True(default), score for player is positive

    Plaese refer to valueTable for more info.

    Notations:
    * is the current position(should be empty)
    0 is empty
    1 is me
    # is opp or out
    $ is opp or out or empty
    & is me or out or empty
    ? is unknown
    """
    if ai:
        me = ME
        opp = OPP
    else:
        me = OPP
        opp = ME
    
    value = 0
    numOfTwo = 0 # number of open 2's

    for i in range(8): # for all 8 directions
        # list of 7, for ?????*??
        lineList = [getline(position, i, -5, board, width, height),\
            getline(position, i, -4, board, width, height),\
                getline(position, i, -3, board, width, height),\
                    getline(position, i, -2, board, width, height),\
                        getline(position, i, -1, board, width, height),\
                            getline(position, i, 1, board, width, height),\
                                getline(position, i, 2, board, width, height)]
        
        # value for significant patterns
        if lineList[1:5] == [me, me, me, me]:
            # ?1111*
            if lineList[0] == EMPTY:
                # open 4 01111*
                value += valueTable['OPEN4']
                continue
            else:
                # dead 4A #1111*
                value += valueTable['DEAD4_A']
                continue
        elif lineList[2:5] == [me, me, me]:
            # $111*?
            if lineList[5] == me:
                # dead 4B $111*1
                value += valueTable['DEAD4_B']
                continue
            elif lineList[5] == EMPTY:
                # $111*0
                if lineList[1] == EMPTY:
                    # open 3A 0111*0
                    value += valueTable['OPEN3_A']
                    continue
                else:
                    # dead 3A #111*0
                    value += valueTable['DEAD3_A']
                    continue
            else:
                # $111*#
                if lineList[1] == EMPTY:
                    # open 3B 0111*#
                    value += valueTable['OPEN3_B']
                    continue
        elif lineList[1:5] == [me, me, me, EMPTY]:
            # open 3C 1110*
            value += valueTable['OPEN3_C']
            continue
        elif lineList[3:6] == [me, me, me]:
            # $11*1? (111*1 solved by dead 4B)
            if lineList[6] == me:
                # dead 4C $11*11
                value += valueTable['DEAD4_C']
                continue
            elif lineList[6] == EMPTY:
                # $11*10
                if lineList[2] == EMPTY:
                    # dead 3B 011*10
                    value += valueTable['DEAD3_B']
                    continue
                else:
                    # dead 3D1 #11*10
                    value += valueTable['DEAD3_D']
                    continue
            else:
                # $11*1#
                if lineList[2] == EMPTY:
                    # dead 3D2 011*1#
                    value += valueTable['DEAD3_D']
                    continue
                else:
                    # dead 3C #11*1#
                    value += valueTable['DEAD3_C']
                    continue
        
        # number of open 2's
        if lineList[3:5] == [me, me] and lineList[2] != opp and lineList[5] != opp:
            # &11*& where &:me|out|empty
            numOfTwo += 1

        # value for all other patterns
        numOfMe = 0
        for k in range(-4,1):
            # ++++*, +++*+, ++*++, +*+++, *++++
            tmp = 0
            for l in range(5):
                x = getline(position, i, k+l, board, width, height)
                if x == me:
                    tmp += 1
                elif x == opp or x == OUT:
                    tmp = 0
                    break
            numOfMe += tmp
        value += numOfMe * 15

    if numOfTwo >= 2:
        value += valueTable['MULTI_OPEN2']

    return value


def evaluate_player(position, board, width, height, player):
    """
    evaluate the board if player put next piece at position(x,y)
    player is the current player being scored
    evaluate for ME

    Plaese refer to valueTable for more info.

    Notations:
    * is the current position(should be empty)
    0 is empty
    1 is me
    # is opp or out
    $ is opp or out or empty
    & is me or out or empty
    ? is unknown
    """
    if player == ME:
        opp = OPP
    else:
        opp = ME
    
    value = 0
    numOfTwo = 0 # number of open 2's

    for i in range(8): # for all 8 directions
        # list of 7, for ?????*??
        lineList = [getline(position, i, -5, board, width, height),\
            getline(position, i, -4, board, width, height),\
                getline(position, i, -3, board, width, height),\
                    getline(position, i, -2, board, width, height),\
                        getline(position, i, -1, board, width, height),\
                            getline(position, i, 1, board, width, height),\
                                getline(position, i, 2, board, width, height)]
        
        # value for significant patterns
        if lineList[1:5] == [player, player, player, player]:
            # ?1111*
            if lineList[0] == EMPTY:
                # open 4 01111*
                value += valueTable['OPEN4']
                if player != ME:
                    value -= 500
                continue
            else:
                # dead 4A #1111*
                value += valueTable['DEAD4_A']
                if player != ME:
                    value -= 500
                continue
        elif lineList[2:5] == [player, player, player]:
            # $111*?
            if lineList[5] == player:
                # dead 4B $111*1
                value += valueTable['DEAD4_B']
                if player != ME:
                    value -= 500
                continue
            elif lineList[5] == EMPTY:
                # $111*0
                if lineList[1] == EMPTY:
                    # open 3A 0111*0
                    value += valueTable['OPEN3_A']
                    continue
                else:
                    # dead 3A #111*0
                    value += valueTable['DEAD3_A']
                    continue
            else:
                # $111*#
                if lineList[1] == EMPTY:
                    # open 3B 0111*#
                    value += valueTable['OPEN3_B']
                    continue
        elif lineList[1:5] == [player, player, player, EMPTY]:
            # open 3C 1110*
            value += valueTable['OPEN3_C']
            continue
        elif lineList[3:6] == [player, player, player]:
            # $11*1? (111*1 solved by dead 4B)
            if lineList[6] == player:
                # dead 4C $11*11
                value += valueTable['DEAD4_C']
                continue
            elif lineList[6] == EMPTY:
                # $11*10
                if lineList[2] == EMPTY:
                    # dead 3B 011*10
                    value += valueTable['DEAD3_B']
                    continue
                else:
                    # dead 3D1 #11*10
                    value += valueTable['DEAD3_D']
                    continue
            else:
                # $11*1#
                if lineList[2] == EMPTY:
                    # dead 3D2 011*1#
                    value += valueTable['DEAD3_D']
                    continue
                else:
                    # dead 3C #11*1#
                    value += valueTable['DEAD3_C']
                    continue
        
        # number of open 2's
        if lineList[3:5] == [player, player] and lineList[2] != opp and lineList[5] != opp:
            # &11*& where &:me|out|empty
            numOfTwo += 1

        # value for all other patterns
        numOfPlayer = 0
        for k in range(-4,1):
            # ++++*, +++*+, ++*++, +*+++, *++++
            tmp = 0
            for l in range(5):
                x = getline(position, i, k+l, board, width, height)
                if x == player:
                    tmp += 1
                elif x == opp or x == OUT:
                    tmp = 0
                    break
            numOfPlayer += tmp
        value += numOfPlayer * 15

    if numOfTwo >= 2:
        value += valueTable['MULTI_OPEN2']
        if player != ME:
            value -= 100

    return value

def evaluate(position, board, width, height):
    myScore = [[0 for i in range(height)] for j in range(width)]
    oppScore = [[0 for i in range(height)] for j in range(width)]
    myMaxScore = 0
    oppMaxScore = 0

    for x in range(width):
        for y in range(height):
            position = (x, y)

    myMaxScore
    valueMe = evaluate_player(position, board, width, height, ME)
    valueOpp = evaluate_player(position, board, width, height, OPP)
    return valueMe + valueOpp