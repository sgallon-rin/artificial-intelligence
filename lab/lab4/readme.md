## Lab 4: Exact Inference

### files
* inferences-template.py: template
* inference.py: solution
* description.txt: task description, including test input and output

### DESCRIPTION

Implement enumeration algorithm and variable elimination algorithm for answering queries on Bayesian networks. 
In this problem, we assume that all nodes in the Bayesian net only have two values, “+” (occurred) and “-” (not occurred) 

### INPUT

The input consists of several queries (one query per line, asking for specific joint probabilities, marginal probabilities, or conditional probabilities), and evidences after them. 

The line between queries and evidences have “\*\*\*\*\*\*” (six stars) as the separator. The following lines represent a Bayesian net by showing the tables of probabilities or conditional probabilities for each node. The tables are separated by “\*\*\*” (three stars). 

The first line contains the node’s name, followed by the names of its parents, separated by “|”. All node names begin with an uppercase letter and contains letter only. 

The following lines show the probabilities given all combinations of parent node values. The probability is always for occurrence (“+”) only, and you can compute the probability of nonoccurrence (“-”). 

### OUTPUT

For each query in the input, output the corresponding probability, rounded two decimals, and separated by “\*\*\*\*\*\*\*\*\*\*” (ten stars) 

### SAMPLE INPUT

P(Earthquake = -)

P(Burglary = + | John = +, Mary = +)

\*\*\*\*\*\*

Burglary

0.001

\*\*\*

Earthquake

0.002

\*\*\*

Alarm | Burglary Earthquake

0.95 + +

0.94 + -

0.29 - +

0.001 - -

\*\*\*

John | Alarm

0.9 +

0.05 -

\*\*\*

Mary | Alarm

0.7 +

0.01 –

### SAMPLE OUTPUT
probability by enumeration:  1.0

probability by elimination:  1.0

\*\*\*\*\*\*\*\*\*\*

probability by enumeration:  0.28

probability by elimination:  0.28

\*\*\*\*\*\*\*\*\*\*
