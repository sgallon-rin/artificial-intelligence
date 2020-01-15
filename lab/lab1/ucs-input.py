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
        actions_state = []
        actions = self.actions
        for act in actions:
            if act[0] == state:
                actions_state.append(act)
        return actions_state

    def solution(self, node):
        path = []
        while node.parent:
            path.append(node.state)
            node = node.parent
        #endwhile
        path.append(self.initial_state)
        return path[::-1]

    def transition(self, state, action):
        if state == action[0]:
            return action[1]
        else:
            print("Step error!")
            raise Exception
            #sys.exit()	

    def goal_test(self, state):
        return state == 'Goal'

    def step_cost(self, state1, action, state2):
        if (state1 == action[0]) and (state2 == action[1]):
            return int(action[2])
        else:
            print("Step error!")
            raise Exception
            #sys.exit()

    def child_node(self, node_begin, action):
        if node_begin.state == action[0]:
            state = action[1]
            path_cost = node_begin.path_cost + self.step_cost(node_begin.state, action, state)
            node_child = node(state, node_begin, path_cost, action)
            return node_child
        else:
            print("Step error!")
            raise Exception
            #sys.exit()


def UCS(problem):
    node_test = node(problem.initial_state, '', 0, '')
    frontier = PriorityQueue()
    frontier.push(node_test.state, node_test.path_cost)
    in_frontier = [node_test.state]
    state2node = {node_test.state: node_test}
    explored = []
    while not frontier.isEmpty():
        state = frontier.pop()
        in_frontier.remove(state)
        node_present = state2node[state]
        if problem.goal_test(node_present.state):
            return problem.solution(node_present)
        #endif
        if state not in explored:
            explored.append(state)
        #endif
        acts = problem.search_actions(node_present.state)
        for action in acts:
            child = problem.child_node(node_present, action)
            if (child.state not in explored) and (child.state not in in_frontier):
                frontier.push(child.state, child.path_cost)
                in_frontier.append(child.state)
                state2node.update({child.state: child})
            elif child.state in in_frontier:
                old_path_cost = state2node[child.state].path_cost
                if child.path_cost < old_path_cost:
                    frontier.update(child.state, child.path_cost)
                    state2node.update({child.state: child})
                #endif
            #endif
        #endfor
    #endwhile
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
