#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AI final project Gomoku

Name: Jialun Shen
Sid: 16307110030
Name: Jinming Liu
Sid: 17307110101

MCTS(Monte Carlo Tree Search) method
Thia is a UCT(Upper Confidence bound of Tree) version
MCTS is node v
Board is state s

NOTE:
if set time limit to 1 sec
for a board of 10*10
1 simulations in 15.519583940505981 sec (???)
for a board of 20*20
1 simulations in 39.825035095214844 sec
if set time limit to 60 sec
given a board 10*10 with only opp in center
7 simulations in 63.994219064712524 sec
extremely slow!!
so few simulaitonS can by no means converge to the best move!!!
MCTS IS IMPRACTICAL!!
'''

import math, copy, random, time
#import collections
from grader import alive_and_number

MAX_SIM = 5 #maximum number of simulations
TIME_LIMIT = 1 #time limit for each simulation(sec)
#C_UCB = math.sqrt(2) #constant for UCB, see function calculate_UCB()

def calculate_UCB(node, C=math.sqrt(2)):
    """
    calculate the UCB(Upper confidential bound) value for a given node
    C: constant for exploration, default sqrt(2)
    node: a class MCTS node
    UCB = exploitation + exploration
    UCB = W_i/N_i + C * sqrt(ln(N)/N_i)
    UCB = wins / visit + const. * sqrt(ln(parent visit) / visit)
    """
    exploitation_val = node.win_times / node.visited_times
    exploration_val = C * math.sqrt(math.log(node.parent.visited_times) / node.visited_times)
    return exploitation_val + exploration_val


def get_forced_move(board, player, moves, n_in_line=5):
    """
    detect force move for player, return forced move if exist, else None
    forced values: (可以理解为优先级)
        0: no forced aciton(default)
        1: opponent 3-in-a-row 对方三(两头活)(对应number=4!!)
        2: me 3-in-a-row 我方三(两头活)
        3: opp 4-in-a-row 对方四(一头活)
        4: me 4-in-a-row 我方四(一头活)
    NOTE; 
        player 1 first, so take the win action first
        the number alive_and_number returns include the new one at move
    """
    #forced = collections.defaultdict(int)
    opp = 3 - player
    move4 = dict()
    move3 = dict() #需要考虑number的大小
    move2 = []
    move1 = []
    for move in moves:
        for d in range(4):
            alive, number = alive_and_number(board, player, move, d, n_in_line)
            if alive >= 1 and number >=5:
                # forced[move] = max(4, forced[move])
                # return move
                if move in move4.keys():
                    move4[move] = max(number, move4[move])
                else:
                    move4[move] = number
            elif alive == 2 and number == 4:
                # forced[move] = max(2, forced[move])
                if move not in move2:
                    move2.append(move)
            alive, number = alive_and_number(board, opp, move, d, n_in_line)
            if alive >= 1 and number >=5:
                # forced[move] = max(2, forced[move])
                if move in move3.keys():
                    move3[move] = max(number, move3[move])
                else:
                    move3[move] = number
            elif alive == 2 and number == 4:
                # forced[move] = max(1, forced[move])
                if move not in move1:
                    move1.append(move)
    # try:
    #     forced_move = max(forced)
    #     assert forced[forced_move] > 0, "forced move error!"
    # except:
    #     forced_move = None
    if move4:
        forced_move_max_num = max(move4.values())
        forced_move = random.choice([k for k in move4.keys() if move4[k] == forced_move_max_num])
    elif move3:
        forced_move_max_num = max(move3.values())
        forced_move = random.choice([k for k in move3.keys() if move3[k] == forced_move_max_num])
    elif move2:
        forced_move = random.choice(move2)
    elif move1:
        forced_move = random.choice(move1)
    else:
        forced_move = None
    # print(move4, move3, move2, move1)
    return forced_move


class MCTS:
    """
    class of a Monte Carlo Tree Search state node
    Attributes:
        board: a class Board object
        players: (p1, p2), p1 will move next, whose opponent is p2
        move: a move this node has taken form parent(None if this is a root Node, i.e., self.parent is None)
        parent: parent Node
        successor: list of Node representing children of the current node
    """
    def __init__(self, board, players=(1,2), move=None, parent=None, successor=None):
        self.board = board
        self.players = players
        self.move = move # move from parent node
        self.visited_times = 0
        self.win_times = 0
        self.parent = parent
        if successor is None:
            successor  = []
        self.successor = successor
        #self.tried = collections.defaultdict(bool) # dict of moves of successors

    def is_all_expand(self):
        """whether all possive moves(child nodes) have been expanded"""
        return len(self.successor) == len(self.board.possible_moves)
    
    def add_successor_from_move(self, move):
        """add a successor from a move (x,y), return the successor node(class MCTS)"""
        s_Board = copy.deepcopy(self.board)
        s_Board.player_move(self.players[0], move)
        s_Board.player = self.players[1]
        s_Board.possible_moves = s_Board.get_possible_moves()
        s_players = self.players[::-1]
        s = MCTS(s_Board, s_players, move, parent=self)
        self.successor.append(s)
        #self.tried[move] = True
        return s

    def is_terminal(self):
        """whether this node is a leaf node"""
        return self.board.is_terminal()

    def visited_times_add_one(self):
        self.visited_times += 1

    def win_times_add_reward(self, reward):
        """NOTE: reward should be either 1(win) or 0(lose)"""
        self.win_times += reward

    def get_untried_moves(self):
        """get untrued moves"""
        if self.successor:
            untried_moves = []
            tried_moves = [sub_node.move for sub_node in self.successor]
            all_moves = self.board.possible_moves
            for move in all_moves:
                if move not in tried_moves:
                    untried_moves.append(move)
            return untried_moves
        else:
            return self.board.possible_moves


class Board:
    """
    class of a Board, attribute of a MCTS node
    Attributes:
        board: a list of board
        n_in_line: number of chess in a line to win
    NOTICE:
        This Board is different from the one in minimax.py
        Every time you create a Board, it will automatically get its possible moves
    """
    def __init__(self, board, n_in_line=5):
        self.board = board
        self.width = len(board) #对应x
        self.height = len(board[0]) #对应y
        self.n_in_line = n_in_line
        self.possible_moves = self.get_possible_moves()

    def isBoard(self, position):
        """check whether position is on board (False if out of board)"""
        x, y = position
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def isFree(self, position):
        """check whether position is free"""
        return self.isBoard(position) and self.board[position[0]][position[1]] == 0

    def isOccupied(self, position):
        """check whether position is occupied"""
        return self.isBoard(position) and self.board[position[0]][position[1]] > 0

    def get_occupied_positions(self):
        """get occupied positions (x,y) on current board"""
        positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.isOccupied((x,y)):
                    positions.append((x,y))
        return positions

    def get_possible_moves(self):
        """
        return all posible free positions the next move can take
        we consider possible moves to be positions within 2 empty positions from all occupied positions
        """
        positions = []
        emptyBoard = True
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] != 0:
                    emptyBoard = False
                    for i in range(self.n_in_line):
                        for j in range(self.n_in_line):
                            newPosition = (x+i-2, y+j-2)
                            if self.isFree(newPosition) and newPosition not in positions:
                                positions.append(newPosition)
        if emptyBoard:
            # return the center position if the board is empty
            positions.append((self.width//2, self.height//2))
        return positions

    def get_random_move(self):
        """get next move with random choice"""
        return random.choice(self.possible_moves)

    def player_move(self, player, move):
        """move for player"""
        # if not self.isFree(move):
        #     self.print_board()
        #     print(move)
        #     print(move in self.possible_moves)
        assert self.isFree(move), "Invalid move!!"
        assert player in (1, 2), "Invalid player!!"
        self.board[move[0]][move[1]] = player
    
    def print_board(self):
        for line in self.board:
            print(line)

    def check_win_at_pos(self, position):
        """
        check if any player wins (is a terminal state) at position
        position should not be free
        return win player (1 or 2), or 0 if nobody wins
        """
        x_this, y_this = position
        # get the boundaries
        up = min(x_this, self.n_in_line - 1)
        down = min(self.height - 1 - x_this, self.n_in_line - 1)
        left = min(y_this, self.n_in_line - 1)
        right = min(self.width - 1 - y_this, self.n_in_line - 1)
        # \
        up_left = min(up, left)
        down_right = min(down, right)
        for i in range(up_left + down_right - self.n_in_line + 2):
            a = [
                self.board[x_this - up_left + i + j][y_this - up_left + i + j] for j in range(self.n_in_line)
            ]
            assert len(a) == self.n_in_line, "error when check if win on board"
            if len(set(a)) == 1 and a[0] > 0:
                return a[0]
        # /
        up_right = min(up, right)
        down_left = min(down, left)
        for i in range(up_right + down_left - self.n_in_line + 2):
            a = [
                self.board[x_this - up_right + i + j][y_this + up_right - i - j] for j in range(self.n_in_line)
            ]
            assert len(a) == self.n_in_line, "error when check if win on board"
            if len(set(a)) == 1 and a[0] > 0:
                return a[0]
        # --
        for i in range(left + right - self.n_in_line + 2):
            a = [
                self.board[x_this][y_this - left + i + j] for j in range(self.n_in_line)
            ]
            assert len(a) == self.n_in_line, "error when check if win on board"
            if len(set(a)) == 1 and a[0] > 0:
                return a[0]
        # |
        for i in range(up + down - self.n_in_line + 2):
            a = [
                self.board[x_this - up + i + j][y_this] for j in range(self.n_in_line)
            ]
            assert len(a) == self.n_in_line, "error when check if win on board"
            if len(set(a)) == 1 and a[0] > 0:
                return a[0]
        # no one wins
        return 0

    def check_win(self):
        """
        check if any player wins (is a terminal state) on the whole board
        position should not be free
        return win player (1 or 2), or 0 if nobody wins
        """
        check_pos = self.get_occupied_positions()
        winner = 0
        if not check_pos:
            # empty board, nobody wins
            return winner
        for pos in check_pos:
            winner = self.check_win_at_pos(pos)
            if winner > 0:
                return winner
        return winner

    def is_terminal(self):
        """whether this state is a terminal state"""
        return self.check_win() > 0

    def get_reward(self):
        """
        get the reward if game is over
        reward is 1 if AI(player with color 1) wins, else 0
        """
        winner = self.check_win()
        if winner == 0:
            return 0
        #assert self.is_terminal(), "ERROR for get_reward! Game is not over!"
        return 1 if winner == 1 else 0

    def force(self, player):
        """get forced move for player"""
        return get_forced_move(self.board, player, self.possible_moves, self.n_in_line)


def tree_policy(node):
    """
    1 Selection Phase
    find a best node under tree policy from the given node
    Args:
        node: a class MCTS node
    Returns:
        a class MCTS node
    NOTICE:
    Tree Policy: 根据exploration/exploitation算法返回最好的需要expend的节点
    注意：如果节点是叶子结点直接返回。
    基本策略是先找当前未选择过的子节点，如果有多个则随机选。
    如果都选择过就找权衡过exploration/exploitation的UCB值最大的，
    如果UCB值相等则随机选。
    """
    begin_time = time.time()
    # Check if the current node is the leaf node
    while not node.is_terminal() and time.time()-begin_time < TIME_LIMIT:
        #print("tree policy")
        if node.is_all_expand():
            node = best_child(node)
        else:
        # Return the new sub node (expand)
            sub_node = expand(node)
            return sub_node
    # Return the leaf node, this is the best child node
    return node


def policy(node):
    """
    Args:
        node: a class MCTS node!!! not Board as in pesudocode
    Returns:
        int, reward for state
    """
    # Get the state of the game (a class Board object)
    begin_time = time.time()
    board = copy.deepcopy(node.board)
    players = copy.deepcopy(node.players)
    # Run until the game over
    while not board.is_terminal() and time.time()-begin_time < TIME_LIMIT:
        # if satisfied with heuristic knowledge, then obtain forced action
        # else, pick one random action to play and get next state
        #print("policy")
        move = board.force(players[0]) #forced_move
        if not move:
            move = board.get_random_move()
        board.player_move(players[0], move)
        board.possible_moves = board.get_possible_moves()
        players = players[::-1]
    # terminal state, get reward
    reward = board.get_reward()
    return reward


def expand(node):
    """
    2 Expantion Phase
    Args:
        node: a class MCTS node
    Returns:
        a class MCTS successor node just expanded
    输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点。注意，需要保证新增的节点与其他节点Action不同。
    """
    # Get a new state which has the different action from others, i.e., not tried
    forced_move = node.board.force(node.players[0])
    if forced_move:
        if forced_move in node.get_untried_moves():
            sub_node = node.add_successor_from_move(forced_move)
        else:
            for successor in node.successor:
                if successor.move == forced_move:
                    sub_node = successor
                    break
    else:
        new_move = random.choice(node.get_untried_moves())
        sub_node = node.add_successor_from_move(new_move)
    return sub_node


def best_child(node):
    """
    argmax_{child_node} UCB(node)
    使用UCB算法，权衡exploration和exploitation后选择得分最高的子节点，
    注意如果是预测阶段直接选择当前win值最高的。
    """
    best_score = float("-inf")
    best_sub_node = None
    # Travel through all sub nodes to find the best one
    for sub_node in node.successor:
        score = calculate_UCB(sub_node)
        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    return best_sub_node


def back_update(node, reward):
    """
    4 Backpropagation Phase
    阶段，输入前面获取需要expend的节点和新执行Action的reward，反馈给expend节点和上游所有节点并更新对应数据。
    """
    # Update util the root node
    while node:
        # Update the visit times
        node.visited_times_add_one()
        # Update the quality value
        node.win_times_add_reward(reward)
        # Change the node to the parent node
        node = node.parent


def MCTS_UCT(node, max_sim=MAX_SIM, time_limit=TIME_LIMIT):
    """
    main  process of MCTS, find the best move for given board list
    Args:
        node: a class MCTS node
        n: int, the height of tree(including root)
    Returns:
        a move (x, y)

    实现蒙特卡洛树搜索算法，传入一个根节点，在有限的时间内根据之前已经探索过的树结构expand新节点和更新数据，
    然后返回只要exploitation最高的子节点。
    蒙特卡洛树搜索包含四个步骤，Selection、Expansion、Simulation、Backpropagation。
    前两步使用tree policy找到值得探索的节点。
    第三步使用default policy也就是在选中的节点上随机算法选一个子节点并计算reward。
    最后一步使用backup也就是把reward更新到所有经过的选中节点的节点上。
    进行预测时，只需要根据Q值选择exploitation最大的节点即可，找到下一个最优的节点。
    """
    begin_time = time.time()
    i = 1 #number of simulations
    # Run as much as possible under the computation budget
    while time.time() - begin_time <= time_limit and i <= max_sim:
        # 1. Find the best node to expand
        expand_node = tree_policy(node)
        # 2. Random run to add node and get reward
        reward = policy(expand_node)
        # 3. Update all passing nodes with reward
        back_update(expand_node, reward)
        i += 1
    # N. Get the best next node
    best_next_node = best_child(node)
    #print("{} simulations in {} sec".format(i-1, time.time()-begin_time))
    return best_next_node


def find_move(board, max_sim=MAX_SIM, time_limit=TIME_LIMIT):
    """
    find the best move for given board list
    Args:
        board: a board list
        max_sim: maximum number of simulations
        time_limit: time limit for each simulation(sec)
    Returns:
        a move (x, y)
    """
    root = MCTS(Board(board))
    best_next_node = MCTS_UCT(root, max_sim, time_limit)
    best_next_move = best_next_node.move
    #root.board.print_board()
    #root.board.player_move(1, best_next_move)
    #print("best move found by MCTS is ", best_next_move)
    #root.board.print_board()
    return best_next_move


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
    b = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,2,2,2,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
         ]
    c = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
         ]
    c1 = [[0 for i in range(10)] for j in range(10)]
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
    # B = Board(a)
    # B.print_board()
    # best_next_move = get_forced_move(B.board, 1, B.possible_moves)
    # print("\nbest move found by MCTS is {}\n".format(best_next_move))
    # B.player_move(1, best_next_move)
    # B.print_board()
    print(find_move(a))
    print(find_move(b))
    print(find_move(c))
    print(find_move(d))
    print(find_move(c1))