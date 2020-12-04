#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
AI final project Gomoku

Name: Jialun Shen
Sid: 16307110030
Name: Jinming Liu
Sid: 17307110101

Minmax with Alpha-Beta Pruning
for a board 20*20
approx. 0.3 sec per move if n=2(search depth = 1), 60 sec if n=3(search depth = 2)
however, approx. 7 sec per move if n=2 in practice on piskvork.exe
'''

import copy
import grader

MAX = grader.MAX_POINT
MIN = -1 * MAX

class Board:
    """class of a Board, node of the tree.
    Attributes:
        board: a list of board
        n_in_line: number of chess in a line to win
        players: (p1, p2), p1 will move next, whose opponent is p2
        move: a move this node has taken(None if this is a root Node, i.e., self.parent is None)
        parent: parent Node
        successor: list of Node representing children of the current node
        is_leaf: bool, whether the node is a leaf or not(game is over of reach the depth limit)
    """
    def __init__(self, board, n_in_line=5, players=(1,2), move=None, parent=None, successor=None, is_leaf=False):
        self.board = board
        self.width = len(board) #对应x
        self.height = len(board[0]) #对应y
        self.n_in_line = n_in_line
        self.players = players
        if players[0] == 1:
            self.rule = "max"
        else:
            self.rule = "min"
        if successor is None:
            successor = []
        self.parent = parent
        self.successor = successor
        self.is_leaf = is_leaf
        self.move = move

    def isFree(self, position):
        """check whether position is free"""
        x, y = position
        return x >= 0 and y >= 0 and x < self.width and y < self.height and self.board[x][y] == 0

    def evaluate(self, moves):
        """
        evaluate the current board given a list of next moves(start with ME)
        this is the leaf node value for the child Board len(moves) deeper
        """
        return grader.eval_individual(self.board, self.players, moves, self.n_in_line)

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

    def grow(self):
        """grow a layer deeper"""
        possible_moves = self.get_possible_moves()
        for move in possible_moves:
            #print(move)
            x, y = move
            s_board = copy.deepcopy(self.board)
            s_board[x][y] = self.players[0]
            s_players = self.players[::-1]
            successor_Board = Board(board=s_board, n_in_line=self.n_in_line, players=s_players, move=move, parent=self)
            self.successor.append(successor_Board)
        #print(self.board, "grow successful")


def get_moves_from_root(node):
    """
    node: a class Board object
    get the list of moves taken from root to node
    """
    moves = []
    while node.parent is not None:
        moves.append(node.move)
        node = node.parent
    moves.reverse()
    #print(moves)
    return moves


# class MoveSeq:
#     """class of move sequence"""
#     def __init__(self, moves, parent=None, successor=None):
#         if successor is None:
#             successor = []
#         self.moves = moves
#         self.parent = parent
#         self.successor = successor

#     def new_move(self, newMove):
#         newMoves = copy.deepcopy(self.moves)
#         newMoves.append(newMove)
#         successor_MoveSeq = MoveSeq(newMoves, parent=self)
#         self.successor.append(successor_MoveSeq)


def get_value_and_move(node, alpha, beta, root):
    """Get value for the given moveseq at root
    Args:
        moveseq: class MoveSeq object
        alpha: float
        beta: float
        node: a class Board object(should be root of the Board tree)
    Returns:
        value of the moveseq at node
    Actually we always call max_value first in Gomoku
    """
    if node.rule == 'max':
        return max_value_and_move(node, alpha, beta, root)
    else:
        return min_value_and_move(node, alpha, beta, root)


def max_value_and_move(node, alpha, beta, root):
    """Get value for the given MAX node,
    also the move sequence
    Args:
        node: class Board object
        alpha: float
        beta: float
        root: class Board object, root of the search tree(for evaluation)
    Returns:
        value of the node
        move sequence to the node [(x1,y1),(x2,y2),...]
    """
    if node.is_leaf:
        moves = get_moves_from_root(node)
        return root.evaluate(moves), moves
    v = float("-inf")
    moveseq = []
    for successor in node.successor:
        s_value, s_moveseq = min_value_and_move(successor, alpha, beta, root)
        #v = max(v, s_value)
        if s_value >= v:
            v = s_value
            moveseq = s_moveseq
        if v >= beta:
            #print(v, moveseq)
            return v, moveseq
        alpha = max(alpha, v)
    #print(v, moveseq)
    return v, moveseq


def min_value_and_move(node, alpha, beta, root):
    """Get value for the given MIN node,
    also the move sequence
    Args:
        node: class Board object
        alpha: float
        beta: float
        root: class Board object, root of the search tree(for evaluation)
    Returns:
        value of the node
        move sequence to the node [(x1,y1),(x2,y2),...]
    """
    if node.is_leaf:
        moves = get_moves_from_root(node)
        return root.evaluate(moves), moves #no need to times (-1) here
    v = float("inf")
    moveseq = []
    for successor in node.successor:
        s_value, s_moveseq = max_value_and_move(successor, alpha, beta, root)
        #v = min(v, s_value)
        if s_value <= v:
            v = s_value
            moveseq = s_moveseq
        if v <= alpha:
            #print(v, moveseq)
            return v, moveseq
        beta = min(beta, v)
    #print(v, moveseq)
    return v, moveseq


def construct_tree(board, n):
    """Construct a tree using given information and return the root node.
    Args:
        n: int, the height of tree
        board: a board list
    Returns:
        root node
    """
    root = Board(board=board)
    grow_tree(root, n)
    #print("construcion of tree with depth {} successful!".format(n))
    return root


def grow_tree(node, n):
    """
    helper function for construct_tree()
    recusively grow the tree from node, depth is n
    """
    assert n >= 1, "n must be a positive integer!!"
    if n == 1:
        node.is_leaf = True
        return
    node.grow()
    for successor in node.successor:
        grow_tree(successor, n-1)


def find_move(board, n=2):
    """
    find the best move for given board list
    Args:
        board: a board list
        n: int, the height of tree(including root)
    Returns:
        a move (x, y)
    NOTICE:
        default n=2, search depth is 1 layer. (~6sec per move)
        n>=3 is too slow (n=3, ~3min per move)
    """
    assert n > 1, "n must be an integer larger than 1!!"
    root = construct_tree(board, n)
    if len(root.successor) == 1:
        return root.successor[0].move
    valuelst = []
    movelst = []
    for successor in root.successor:
        value, moveseq = get_value_and_move(successor, float("-inf"), float("inf"), root)
        #print(value, moveseq[0])
        valuelst.append(value)
        movelst.append(moveseq[0])
    bestIndex = valuelst.index(max(valuelst))
    bestMove = movelst[bestIndex]
    return bestMove


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
         [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,1,2,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
    #print(find_move(a, n=3))
    #print(find_move(b, n=3))
    #print(find_move(c, n=3))
    # import time
    # begin_time = time.time()
    # print(find_move(d, n=3))
    # print("time used {} sec".format(time.time()-begin_time))
    c1 = [[0 for i in range(20)] for j in range(20)]
    #c1[10][10] = 2
    print(find_move(c1, n=3))