## Lab 3: Reinforcement Learning: Gridworld

### files:
* Gridworld-template.py: template
* Gridworld-synchronous.py: solution, synchronous version
* Gridworld-asynchronous.py: solution, asynchronous version
* input.txt: test input
* output.txt: test solution output

### note:
在值迭代和策略迭代中，可以采用同步和异步两种更新策略。

* 同步(synchronous)更新保存两组状态值向量，在迭代计算时利用上一个时间片的状态向量来更新当前轮次的状态值（按批次更新）；

* 异步(asynchronous)更新仅使用一组状态向量，在迭代计算时采用覆盖操作，即，更新使用的是每个状态最新的状态值。

这两种更新方法会收敛到同样的最优状态值，但是迭代次数不同。

### sample input:
[0,1] [4,1] 10.0

[0,3] [2,3] 5.0

### sample output:
__For synchronous version:__

Value Iteration

number of iterations: 124

22.0 24.4 22.0 19.4 17.5 

19.8 22.0 19.8 17.8 16.0 

17.8 19.8 17.8 16.0 14.4 

16.0 17.8 16.0 14.4 13.0 

14.4 16.0 14.4 13.0 11.7 

&emsp;

Policy Iteration

number of iterations: 8

22.0 24.4 22.0 19.4 17.5 

19.8 22.0 19.8 17.8 16.0 

17.8 19.8 17.8 16.0 14.4 

16.0 17.8 16.0 14.4 13.0 

14.4 16.0 14.4 13.0 11.7 

&emsp;

__For asynchronous version:__

Value Iteration

number of iterations: 29

22.0 24.4 22.0 19.4 17.5 

19.8 22.0 19.8 17.8 16.0 

17.8 19.8 17.8 16.0 14.4 

16.0 17.8 16.0 14.4 13.0 

14.4 16.0 14.4 13.0 11.7 

&emsp;

Policy Iteration

number of iterations: 8

22.0 24.4 22.0 19.4 17.5 

19.8 22.0 19.8 17.8 16.0 

17.8 19.8 17.8 16.0 14.4 

16.0 17.8 16.0 14.4 13.0 

14.4 16.0 14.4 13.0 11.7 
