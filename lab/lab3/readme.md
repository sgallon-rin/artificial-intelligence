## Lab 3: Reinforcement Learning: Gridworld

### files:
* Gridworld-template.py————template
* Gridworld-

### note:
在值迭代和策略迭代中，可以采用同步和异步两种更新策略。

* 同步(synchronous)更新保存两组状态值向量，在迭代计算时利用上一个时间片的状态向量来更新当前轮次的状态值（按批次更新）；

* 异步(asynchronous)更新仅使用一组状态向量，在迭代计算时采用覆盖操作，即，更新使用的是每个状态最新的状态值。

这两种更新方法会收敛到同样的最优状态值，但是迭代次数不同。
