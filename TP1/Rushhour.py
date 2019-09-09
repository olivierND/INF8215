import numpy as np
from collections import deque
import heapq


class Rushhour:

    def __init__(self, horiz, length, move_on, color=None):
        self.nbcars = len(horiz)
        self.horiz = horiz
        self.length = length
        self.move_on = move_on
        self.color = color

        self.free_pos = None

    def init_positions(self, state):
        self.free_pos = np.ones((6, 6), dtype=bool)
        # TODO

    def possible_moves(self, state):
        self.init_positions(state)
        new_states = []
        # TODO
        return new_states

    def solve(self, state):
        visited = set()
        fifo = deque([state])
        visited.add(state)
        # TODO

        return None

    def solve_Astar(self, state):
        visited = set()
        visited.add(state)

        priority_queue = []
        state.h = state.estimee1()
        heapq.heappush(priority_queue, state)

        # TODO
        return None

    def print_solution(self, state):
        # TODO
        return 0