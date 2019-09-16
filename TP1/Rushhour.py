import numpy as np
from collections import deque
import heapq
from State import State


class Rushhour:

    def __init__(self, horiz, length, move_on, color=None):
        self.nbcars = len(horiz) # le nombre de voitures dans la grille;
        self.horiz = horiz
        self.length = length # un vecteur contenant la longueur de chaque voiture (2 ou 3);
        self.move_on = move_on # un vecteur contenant le numéro de la ligne ou la colonne où se trouve la voiture (0-5);
        self.color = color

        self.free_pos = None

    def init_positions(self, state):
        self.free_pos = np.ones((6, 6), dtype=bool)
        for i in range(len(state.pos)):
            if self.horiz[i]:
                for j in range(self.length[i]):
                    self.free_pos[self.move_on[i]][state.pos[i]+j] = False
            else:
                for j in range(self.length[i]):
                    self.free_pos[state.pos[i]+j][self.move_on[i]] = False

    def possible_moves(self, state):
        new_states = []
        self.init_positions(state)
        for i in range(len(state.pos)):
            if self.horiz[i]:
                if state.pos[i] > 0 and self.free_pos[self.move_on[i]][state.pos[i] - 1]:
                    new_states.append(state.move(i, -1))
                if state.pos[i] + self.length[i] < 6 and self.free_pos[self.move_on[i]][state.pos[i] + self.length[i]]:
                    new_states.append(state.move(i, 1))
            else:
                if state.pos[i] > 0 and self.free_pos[state.pos[i]-1][self.move_on[i]]:
                    new_states.append(state.move(i, -1))
                if state.pos[i] + self.length[i] < 6 and self.free_pos[state.pos[i] + self.length[i]][self.move_on[i]]:
                    new_states.append(state.move(i, 1))
        return new_states

    def solve(self, state):
        visited = set()
        fifo = deque([state])
        while len(fifo) > 0:
            current_state = fifo.popleft()

            if current_state not in visited:
                if current_state.success():
                    return current_state

                visited.add(current_state)
                new_states = self.possible_moves(current_state)
                for next_state in new_states:
                    if next_state not in visited:
                        fifo.append(next_state)

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
        i = 1
        fifo = deque([state])
        while state.prev is not None:
            output = str(i) + ". Voiture " + self.color[state.c] + " vers "

            if self.horiz[state.c]:
                if state.d > 0:
                    output += "la gauche."
                else:
                    output += "la droite."
            else:
                if state.d > 0:
                    output += "le bas."
                else:
                    output += "le haut."

            print(output)
            i += 1
            state = state.prev
        return 0