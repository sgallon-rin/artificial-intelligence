# In-class Labs
Each lab has a template, all you need is to fill in th blanks in some key functions.
 
Online evaluation site is [here](http://10.88.3.61)(Unfortunately, you MUST connect the Fudan campus network otherwise you'll have no access to it.)

## 1. Searching: Uniform Cost Search(UCS)
### Description
Write a program for uniform cost search. Find and print the minimum cost path from 'Start' node to 'Goal' node. If there is no answer, please print "Unreachable".

### Input
Each line presents an edge consisting of a tuple of start node, end node and cost. Input ends with 'END'.

### Output
One line for the optimal path in visit order, join by '->'.

### Input Sample
Start A 2

Start B 1

A B 1

A C 3

A D 1

B D 5

B Goal 10

C Goal 7

D Goal 4

END

#### Output sample
Start->A->D->Goal

## 2. Searching: Alpha-Beta Pruning
Implement the following 3 functions:

`def get_value(node, alpha, beta)`

* Choose which function to call

`def max_value(node, alpha, beta)`

`def min_value(node, alpha, beta)`

## 3. Reinforcement Learning: Gridworld

## 4. Probabilistic Graphical Model: Exact Inference
