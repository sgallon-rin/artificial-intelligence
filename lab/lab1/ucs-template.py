import heapq


class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class node:
    """define node"""

    def __init__(self, state, parent, path_cost, action,):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action


class problem:
    """searching problem"""

    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions

    def search_actions(self, state):
	    """Search actions for the given state.

        Args:
            state: a string e.g. 'A'

        Returns:
            a list of action string list
            e.g. [['A', 'B', '2'], ['A', 'C', '3']]
        """
        raise Exception	

    def solution(self, node):
	    """Find th path from the beginning to the given node.

        Args:
            node: the node class defined above.

        Returns:
            ['Start', 'A', 'B', ....]
        """
        raise Exception	

    def transition(self, state, action):
	    """Find the next state from the state adopting the given action.

        Args:
            state: 'A'
            action: ['A', 'B', '2']

        Returns:
            string, representing the next state, e.g. 'B'
		"""
        raise Exception	

    def goal_test(self, state):
	    """Test if the state is goal

        Args:
            state: string, e.g. 'Goal' or 'A'

        Returns:
            a bool (True or False)
        """
        raise Exception	

    def step_cost(self, state1, action, state2):
        if (state1 == action[0]) and (state2 == action[1]):
            return int(action[2])
        else:
            print("Step error!")
            sys.exit()

    def child_node(self, node_begin, action):
	    """Find the child node from the node adopting the given action

        Args:
            node_begin: the node class defined above.
			action: ['A', 'B', '2']

        Returns:
            a node as defined above
        """
        raise Exception	


def UCS(problem):
    """Using Uniform Cost Search to find a solution for the problem.

    Args:
        problem: problem class defined above.

    Returns:
        a list of strings representing the path.
            e.g. ['A', 'B', '2']
        if the path does not exist, return 'Unreachable'
    """
    node_test = node(problem.initial_state, '', 0, '')
    frontier = PriorityQueue()
    frontier.push(node_test.state, node_test.path_cost)
    state2node = {node_test.state: node_test}
    explored = []
    while not frontier.isEmpty():
        raise Exception	
    return "Unreachable"


if __name__ == '__main__':
    Actions = []
    while True:
        a = input().strip()
        if a != 'END':
            a = a.split()
            Actions += [a]
        else:
            break
    graph_problem = problem('Start', Actions)
    answer = UCS(graph_problem)
    s = "->"
    if answer == 'Unreachable':
        print(answer)
    else:
        path = s.join(answer)
        print(path)
