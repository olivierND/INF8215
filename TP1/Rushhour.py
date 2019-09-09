import numpy as np
from collections import deque
import heapq
from State import State


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
                for j in range(0, self.length[i]):
                    self.free_pos[self.move_on[i]][state.pos[i]+j] = False
            else:
                for j in range(0, self.length[i]):
                    self.free_pos[state.pos[i]+j][self.move_on[i]] = False

    def possible_moves(self, state):
        new_states = []
        self.init_positions(state)
        for i in range(0, len(state.pos)):
            if state.pos[i]-1 >= 0 and (self.free_pos[self.move_on[i]][state.pos[i]-1] or self.free_pos[state.pos[i]-1][self.move_on[i]]):
                new_state = State(state.pos)
                new_states.append(new_state.move(i, -1))
            if state.pos[i]+1 < 6 and (self.free_pos[self.move_on[i]][state.pos[i]+1] or self.free_pos[state.pos[i]+1][self.move_on[i]]):
                new_state = State(state.pos)
                new_states.append(new_state.move(i, 1))

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