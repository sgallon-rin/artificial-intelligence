# -*- coding: utf-8 -*-
# __author__ = 'siyuan'
WORLD_SIZE = 5
DISCOUNT = 0.9
# left, up, right, down
ACTIONLIST = ['L', 'U', 'R', 'D']
# actUtil: 'action a' = (index i, increment k)
# after taking action a, increment the element of index i(0: row; 1: column) in position by k.
actUtil = {'L':(1, -1), 'U':(0, -1), 'R':(1, 1), 'D':(0, 1)}


class MDP:
    """The MDP problem.

        Attributes:
            Gird: a dictionary with keys as positions in GridWorld and values equal to 0
            A_POS, A_TO_POS, B_POS, B_TO_POS:
                information of special states, e.g. (0, 1)
            A_REWARD, B_REWARD: float

        Hint:
            We use this class to construct an MDP problem.
    """
    def __init__(self, A_POS, A_TO_POS, A_REWARD, B_POS, B_TO_POS, B_REWARD):
        self.discount = DISCOUNT
        self.world_size = WORLD_SIZE
        self.Grid = dict().fromkeys([(i, j) for i in range(WORLD_SIZE) for j in range(WORLD_SIZE)], 0)
        self.A_POS = A_POS
        self.A_TO_POS = A_TO_POS
        self.A_REWARD = A_REWARD
        self.B_POS = B_POS
        self.B_TO_POS = B_TO_POS
        self.B_REWARD = B_REWARD

    def actions(self, state):
        """ Return set of actions possible from |state|. """
        return ACTIONLIST

    def isSpecial(self, state):
        """ If a state is special """
        if state == self.A_POS:
            return 1
        elif state == self.B_POS:
            return 2
        else:
            return 0

    def getReward(self, state, action):
        """ Return reward of given state and action. """
        if self.isSpecial(state):
            if self.isSpecial(state) == 1:
                return self.A_REWARD
            else:
                return self.B_REWARD
        idx, step = actUtil[action]
        k = state[idx] + step
        r = -1 if (k == -1 or k == self.world_size) else 0
        return r

    def getnewState(self, state, action):
        """ Return new state given state and action. """
        if self.isSpecial(state):
            if self.isSpecial(state) == 1:
                return self.A_TO_POS
            else:
                return self.B_TO_POS
        idx, step = actUtil[action]
        newState = [state[0], state[1]]
        newState[idx] += step
        newState = state if (-1 in newState or self.world_size in newState) else tuple(newState)
        return newState


# value iteration
def value_iteration(MDP):
    """Implement value iteration to compute the optimal values on given MDP.
        Print the optimal value of each state and number of iterations.

        Args:
            MDP: class MDP

        No return

        Hint:
            You can use methods of class MDP to construct this function.

    """
    discount = MDP.discount
    world = MDP.Grid
    # world stores the value of each position in GirdWorld
    iter_num = 0
    while True:
        iter_num += 1
        difference = 0
        # keep iteration until convergence
        # TODO: Begin Your Codes
        for state in world.keys():
            u = world[state]
            maxv = float("-inf")
            maxa = None
            for action in MDP.actions(state):
                r = MDP.getReward(state, action)
                newState = MDP.getnewState(state, action)
                v = r + discount * world[newState]
                if v > maxv:
                    maxv = v
                    maxa = action
            newState = MDP.getnewState(state, maxa)
            r = MDP.getReward(state, maxa)
            world[state] = r + discount * world[newState]
            difference += abs(world[state] - u)
            #if abs(world[state] - u) > difference:
            #    difference = abs(world[state] - u)
        # TODO: End Your Codes
        if difference < 1e-4:
            break

    print('Value Iteration')
    print('number of iterations:', iter_num)
    for i in range(WORLD_SIZE):
        for j in range(WORLD_SIZE):
            print(round(world[(i, j)],1), end=" ")
        print()
    print()


def policy_evaluation(world, policy, MDP):
    """Evaluate the value of each state with fixed policy.

        Args:
            world: GridWorld
            policy: fixed policy, each entry
            MDP: class MDP

        Returns:
            world: Value of each state

        Hint:
            You can use methods of class MDP to construct this function.
    """
    discount = MDP.discount
    while True:
        difference = 0
        # TODO: Begin Your Codes
        for state in world.keys():
            u = world[state]
            action = ACTIONLIST[policy[state]]
            r = MDP.getReward(state, action)
            newState = MDP.getnewState(state, action)
            world[state] = r + discount * world[newState]
            difference += abs(world[state] - u)
            #if abs(world[state] - u) > difference:
            #    difference = abs(world[state] - u)
        # TODO: End Your Codes

        if difference < 1e-4:
            break
    return world


# policy iteration
def policy_iteration(MDP):
    """Implement policy iteration to compute the optimal values on given MDP.
        Print the optimal value of each state and number of iterations.

        Args:
            MDP: class MDP

        No Return

        Hint:
            You can use policy_evaluation and methods of class MDP to construct this function.
    """
    world = MDP.Grid
    # world stores the value of each position in GirdWorld
    policy = dict().fromkeys([(i, j) for i in range(WORLD_SIZE) for j in range(WORLD_SIZE)], 0)
    # initialize policy, take action 'Left'(index 0) at all positions
    discount = MDP.discount
    iter_num = 0
    while True:
        iter_num += 1
        ## TODO:Begin your codes
        world = policy_evaluation(world, policy, MDP)
        unchanged = True
        for state in world.keys():
            maxv = float('-inf')
            maxa = None
            for action in MDP.actions(state):
                r = MDP.getReward(state, action)
                newState = MDP.getnewState(state, action)
                v = r + discount * world[newState]
                if v > maxv:
                    maxv = v
                    maxa = action
            v1 = maxv
            policyAction = ACTIONLIST[policy[state]]
            policyReward = MDP.getReward(state, policyAction)
            policyNewState = MDP.getnewState(state, policyAction)
            v2 = policyReward + discount * world[policyNewState]
            if v1 > v2:
                policy[state] = ACTIONLIST.index(maxa)
                unchanged = False
        if unchanged:
            break
        ## TODO:End your codes

    print('Policy Iteration')
    print('number of iterations:', iter_num)
    for i in range(WORLD_SIZE):
        for j in range(WORLD_SIZE):
            print(round(world[(i, j)],1), end=" ")
        print()


def process_read(x):
    """Read a line of the input.

        Args:
            x: a line of input, string

        Returns:
            from_state: position
            to_state: position
            reward: float
    """
    from_state = (int(x[0][1]), int(x[0][-2]))
    to_state = (int(x[1][1]), int(x[1][-2]))
    reward = float(x[-1])
    return from_state, to_state, reward


while True:
    try:
        A_list = input().strip().split()
        B_list = input().strip().split()
        A_POS, A_TO_POS, A_REWARD = process_read(A_list)
        B_POS, B_TO_POS, B_REWARD = process_read(B_list)
        MDP1 = MDP(A_POS, A_TO_POS, A_REWARD, B_POS, B_TO_POS, B_REWARD)
        value_iteration(MDP1)
        MDP2 = MDP(A_POS, A_TO_POS, A_REWARD, B_POS, B_TO_POS, B_REWARD)
        policy_iteration(MDP2)
    except EOFError:
        break


# Try to solve Grid World problem based on MDP


