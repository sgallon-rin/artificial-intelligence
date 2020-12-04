#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AI final project Gomoku

Name: Jialun Shen
Sid: 16307110030
Name: Jinming Liu
Sid: 17307110101

grader (evaluation) function for Gomoku AI eggplant(Minimax method ver2)
This is a modified version of a Gomoku evaluation function from Github:
https://github.com/zhangshun97/AI_Gomocup/blob/master/GA/grade.py
with some updates of rules and comments
'''

import copy

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
MAX_POINT = 100000 #point of winning the game
SECOND_MAX = 5000 #point of one step before winning the game
ME = 1
OPP = 2


def find_all_connect(current_board, player, move, n_in_line = 5):
    '''
    以move为中心，找到与player同色且能连接到的子
    Input:
    current_board: a board list
    player: index of player(1/2)
    move: position (x,y)
    n_in_line: number of chess in a line to win
    Output:
    a list of position [(x_1,y_1),...]
    '''
    x_this, y_this = move
    board = copy.deepcopy(current_board)
    width = len(board[0]) #对应y
    height = len(board) #对应x
    # get the boundaries
    up = min(x_this, n_in_line - 1)
    down = min(height - 1 - x_this, n_in_line - 1)
    left = min(y_this, n_in_line - 1)
    right = min(width - 1 - y_this, n_in_line - 1)
    neighbour = [] # 存储与player 能直接到达的且与player同值的坐标
    neighbour.append(move)
    # --
    for i in range(left):
        position = (x_this,y_this-1-i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(right):
        position = (x_this,y_this+1+i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    # \
    up_left = min(up, left)
    down_right = min(down, right)
    for i in range(up_left):
        position = (x_this-1-i,y_this-1-i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(down_right):
        position = (x_this+1+i,y_this+1+i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    # |
    for i in range(up):
        position = (x_this -1 - i, y_this)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(down):
        position = (x_this + 1 + i, y_this)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    # /
    up_right = min(up, right)
    down_left = min(down, left)
    for i in range(up_right):
        position = (x_this - 1 - i, y_this + i + 1)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(down_left):
        position = (x_this + 1 + i, y_this - i - 1)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    return neighbour


def find_direction_connect(current_board, player, move, direction, n_in_line = 5):
    '''
    以move为中心，找到与player同色且能连接到的子，对direciton方向
    Input:
    current_board: a board list
    player: index of player(1/2)
    move: position (x,y)
    dierction: indicator for direction(0:--, 1:|, 2:\, 3:/)
    n_in_line: number of chess in a line to win
    Output:
    a list of position [(x_1,y_1),...]
    '''
    x_this, y_this = move
    board = copy.deepcopy(current_board)
    width = len(board[0]) #对应y
    height = len(board) #对应x
    # get the boundaries
    up = min(x_this, n_in_line - 1)
    down = min(height - 1 - x_this, n_in_line - 1)
    left = min(y_this, n_in_line - 1)
    right = min(width - 1 - y_this, n_in_line - 1)
    neighbour = [] # 存储与player 能直接到达的且与player同值的坐标
    neighbour.append(move)
    if direction == 0:
        # --
        for i in range(left):
            position = (x_this,y_this-1-i)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
        for i in range(right):
            position = (x_this,y_this+1+i)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
    elif direction == 1:
        # |
        for i in range(up):
            position = (x_this -1 - i, y_this)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
        for i in range(down):
            position = (x_this + 1 + i, y_this)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
    elif direction == 2:
        # \
        up_left = min(up, left)
        down_right = min(down, right)
        for i in range(up_left):
            position = (x_this-1-i,y_this-1-i)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
        for i in range(down_right):
            position = (x_this+1+i,y_this+1+i)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
    elif direction == 3:
        # /
        up_right = min(up, right)
        down_left = min(down, left)
        for i in range(up_right):
            position = (x_this - 1 - i, y_this + i + 1)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
        for i in range(down_left):
            position = (x_this + 1 + i, y_this - i - 1)
            if board[position[0]][position[1]] == player:
                neighbour.append(position)
            else:
                break
    return neighbour


def alive_and_number(current_board, player, vertex, direction, n_in_line = 5):
    """
    判断某个棋子(vertex)所在的线是否是活的(一头或两头)，以及活子的个数
    包括形如 X〇XXX (〇为vertex)
    dierction: indicator for direction(0:|, 1:-, 2:\, 3:/), x|v, y->
    Return: 活头数，连续子的个数
    """
    board = copy.deepcopy(current_board)
    width = len(board[0]) #对应y
    height = len(board) #对应x
    dx = [1, 0, 1, 1] # 分别对应四个方向x,y的增加值 [| - \ /]
    dy = [0, 1, 1, -1]
    x, y = vertex
    s = 1 # 这个方向的点总数，包括vertex
    flag1 = 0 # 记录死/活
    flag2 = 0
    # 正方向
    tx = x + dx[direction]
    ty = y + dy[direction]
    while (tx >= 0 and tx < height
            and ty >= 0 and ty < width
            and board[tx][ty] == player) :
        tx += dx[direction]
        ty += dy[direction]
        s += 1
    if(tx >= 0 and tx < height # 判断死活
            and ty >= 0 and ty < width
            and board[tx][ty] == 0):
        flag1 = 1 # 活
    # 反方向
    tx = x - dx[direction]
    ty = y - dy[direction]
    while (tx > 0 and tx < height
            and ty > 0 and ty < width
            and board[tx][ty] == player) :
        tx -= dx[direction]
        ty -= dy[direction]
        s += 1
    if tx >= 0 and tx < height and ty >= 0 and ty < width and board[tx][ty] == 0:
        flag2 = 1

    return flag1 + flag2, s


def eval_vertex(current_board, player, vertex, n_in_line = 5):
    # 对一个顶点进行打分
    board = copy.deepcopy(current_board)
    width = len(board[0]) #对应y
    height = len(board) #对应x
    dx = [1, 0, 1, 1] # 分别对应四个方向x,y的增加值 [- | \ /]
    dy = [0, 1, 1, -1]
    x, y = vertex
    toWin = False
    # assert board[x][y] != player, 'Wrong in find neighbour function!!'
    num = [[0 for i in range(2*n_in_line)] for j in range(2)]
    # num用来记录这个点在各个方向上的布局情况
    # num[a][b]表示有(a+1)个方向是活的、连续同色子长度为b的方向个数
    for i in range(4) : # 4个方向
        s = 1 # 这个方向的点总数，包括在vertex刚刚下的子
        flag1 = 0 # 记录死/活
        flag2 = 0
        # 正方向
        tx = x + dx[i]
        ty = y + dy[i]
        while (tx >= 0 and tx < height
                and ty >= 0 and ty < width
                and board[tx][ty] == player) :
            tx += dx[i]
            ty += dy[i]
            s += 1
        if(tx >= 0 and tx < height # 判断死活
                and ty >= 0 and ty < width
                and board[tx][ty] == 0):
            flag1 = 1 # 活

        # 反方向
        tx = x - dx[i]
        ty = y - dy[i]
        while (tx > 0 and tx < height
                and ty > 0 and ty < width
                and board[tx][ty] == player) :
            tx -= dx[i]
            ty -= dy[i]
            s += 1
        if tx >= 0 and tx < height and ty >= 0 and ty < width and board[tx][ty] == 0:
            flag2 = 1

        if flag1 + flag2 > 0: #至少有一个方向是活的，即可以落子
            num[flag1 + flag2 - 1][s] += 1
        if s >= 5:
            toWin = True
        #print(flag1, flag2, s)

    # 记分
    score = 0
    # 成5（或更多，因为实际上有可能多于5个(比如oooxooo)，已经获胜）
    if sum(num[0][5:]) + sum(num[1][5:]) > 0:
        score = max(score, 100000)
    # 活4 | 双死四 | 死4活3（下一步就能获胜）
    elif num[1][4] > 0 or num[0][4] > 1 or (num[0][4] > 0 and num[1][3] > 0):
        score = max(score, 5000)
    # 双活3
    elif num[1][3] > 1:
        score = max(score, 1000)
    # 死3活3
    elif num[1][3] > 0 and num[0][3] > 0:
        score = max(score, 500)
    # 单活3
    elif num[1][3] > 0:
        score = max(score, 200)
    # 死4
    elif num[0][4] > 0:
        score = max(score, 100)
    # 双活2
    elif num[1][2] > 1:
        score = max(score, 50)
    # 死3
    elif num[0][3] > 0:
        score = max(score, 10)
    # 单活2
    elif num[1][2] > 0:
        score = max(score, 5)
    # 死2
    elif num[0][2] > 0:
        score = max(score, 3)

    # 对局中发现的特殊情况，<白黑黑黑黑〇白>，AI执黑下一步走，明明可以赢了却不下在〇处
    # 该点两头都是死的，因而没有在以上过程计入num
    if toWin:
        score = max(score, 100000)

    return score


def eval_point(current_board, player, point, n_in_line = 5):
    '''
    只考虑进攻，根据player对point打分
    对于所有point的能连接到的邻居，分别打分，取最大值
    '''
    neighbours = find_all_connect(current_board, player, point, n_in_line)
    board = copy.deepcopy(current_board) # 假设这点为player
    board[point[0]][point[1]] = player
    maxvalue = 0
    for neighbour in neighbours:
        value = eval_vertex(board, player, neighbour, n_in_line)
        #print(neighbour, value)
        if value == MAX_POINT:
            return MAX_POINT
        elif value > maxvalue:
            maxvalue = value
    return maxvalue

def eval_move(current_board, players, move, n_in_line = 5):
    '''
    考虑进攻与防守,根据player对move打分
    其实就是对两个player分别打分，然后相加。
    相加（而不是相减）是因为，对敌方有利的位置，敌方得分高，我方应防守
    '''
    assert current_board[move[0]][move[1]] == 0, "There exists one chess already!!!"
    tempt1 = eval_point(current_board, players[0], move, n_in_line)
    tempt2 = eval_point(current_board, players[1], move, n_in_line)
    return tempt1 + tempt2, tempt1 == MAX_POINT or tempt1 == SECOND_MAX
    #return tempt1 + tempt2

def eval_individual(board, players, moves, n_in_line = 5):
    '''
    给个体打分，对一系列的棋步[(x1,y1),(x2,y2),...]（ME->OPP->ME->...）进行打分
    players = [ME, OPP] 如果ME先手，vice versa
    len(moves) 等于 搜索树高度
    实际上第一步始终是ME, 结果得分ME的得分为正
    '''
    if len(set(moves)) != len(moves):
        return -1
    current_board = copy.deepcopy(board)
    players = list(players)
    value = 0
    if players[0] == ME:
        sign = 1
    else:
        sign = -1
    me_win = False # Ai win
    opp_win = False # opp win
    for move in moves:
        if me_win:
            value += 2 * MAX_POINT
        elif opp_win:
            value -= 2 * MAX_POINT
        else:
            evaluation = eval_move(current_board, players, move, n_in_line)
            if evaluation[1]: # 处理一方胜利的情况/一方出现4并且下一步是该方的情况
                if players[0] == ME: # AI赢了
                    me_win = True
                else: # 对手赢了
                    opp_win = True
            value += sign * evaluation[0] # evaluate one move
            current_board[move[0]][move[1]] = players[0] # 'put' one chess
            sign = -sign
            players.reverse()
    return value


if __name__ == "__main__":
    a = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,2,0,2,2,2,2,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
         ]
    d = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 1, 1, 1, 0, 2, 2, 1, 2, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 0, 1, 1, 2, 2, 2, 2, 1, 2, 0, 2, 0, 0, 0, 0],
        [0, 0, 1, 1, 2, 2, 1, 2, 0, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    d = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 1, 1, 1, 0, 2, 2, 1, 2, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 0, 1, 1, 2, 2, 2, 2, 1, 2, 0, 2, 0, 0, 0, 0],
        [0, 0, 1, 1, 2, 2, 1, 2, 0, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    #print(eval_point(d,1,(6,1),5))
    print(eval_point(d,2,(6,1),5))
    # d[6][1] = 1
    # for line in d:
    #     print(line)
    #print(eval_move(a,[1,2],(7,7),5))
    #print(eval_individual(a, [ME, OPP], [(7,7),(7,2),(10,7),(5,5)], 5))