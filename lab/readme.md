# In-class Labs
Each lab has a template, all you need is to fill in th blanks in some key functions.
 
Online evaluation and task description site is [here](http://10.88.3.61)(Unfortunately, you MUST connect the Fudan campus network.)

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

### Output sample
Start->A->D->Goal

## 2. Searching: Alpha-Beta Pruning
Implement the following 3 functions:

`def get_value(node, alpha, beta)`

* Choose which function to call

`def max_value(node, alpha, beta)`

`def min_value(node, alpha, beta)`

## 3. Reinforcement Learning: Gridworld
### Problem:
Solve the Grid World Problem based on MDP

### Requirement:
Print the iteration numbers and optimal values of all states using value iteration and policy iteration

### Address: [here](http://10.88.3.61/problem.php?cid=1003&pid=0)(requires Fudan campus network)

## 4. Probabilistic Graphical Model: Exact Inference
### Review on exact inference algorithm:
#### Example: MaryCall , JohnCall in Ch14 of textbook
#### Enumeration algorithm:
• Step 1: Select the entries consistent with the evidence

• Step 2: Sum out hidden vars to get joint of Query and evidence

• Step 3: Normalize

#### Elimination algorithm:
• Make factors

• Join all factors and eliminate all hidden vars




