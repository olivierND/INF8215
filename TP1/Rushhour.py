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

        for i in range(0, len(state.pos)):
            if self.horiz[i]:
                second_index = state.pos[i]
                first_index = self.move_on[i]
                for j in range(0, self.length[i]):
                    self.free_pos[first_index][second_index+j] = False
            else:
                second_index = self.move_on[i]
                first_index = state.pos[i]
                for j in range(0, self.length[i]):
                    self.free_pos[first_index+j][second_index] = False

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