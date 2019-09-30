import numpy as np
from collections import deque
import heapq
from State import State


class Rushhour:

    def __init__(self, horiz, length, move_on, color=None):
        # Le nombre de voitures dans la grille;
        self.nbcars = len(horiz)

        # Si la voiture est horizontale
        self.horiz = horiz

        # Un vecteur contenant la longueur de chaque voiture (2 ou 3);
        self.length = length

        # Un vecteur contenant le numéro de la ligne ou la colonne où se trouve la voiture (0-5);
        self.move_on = move_on

        # Couleur
        self.color = color

        self.free_pos = None

    def init_positions(self, state):
        self.free_pos = np.ones((6, 6), dtype=bool)
        for i in range(len(state.pos)):
            if self.horiz[i]:
                for j in range(self.length[i]):
                    # Row reste toujours cst, +j pour ajouter le length de l'auto
                    self.free_pos[self.move_on[i]][state.pos[i]+j] = False
            else:
                for j in range(self.length[i]):
                    # Column reste toujours cst, +j pour ajouter le length de l'auto
                    self.free_pos[state.pos[i]+j][self.move_on[i]] = False

    def possible_moves(self, state):
        new_states = []
        self.init_positions(state)
        for i in range(len(state.pos)):
            if self.horiz[i]:
                # Regarder pour reculer (vers la gauche)
                if state.pos[i] > 0 and self.free_pos[self.move_on[i]][state.pos[i] - 1]:
                    new_states.append(state.move(i, -1))
                # Regarder pour avancer (vers la droite)
                if state.pos[i] + self.length[i] < 6 and self.free_pos[self.move_on[i]][state.pos[i] + self.length[i]]:
                    new_states.append(state.move(i, 1))
            else:
                # Regarder pour reculer (vers le bas)
                if state.pos[i] > 0 and self.free_pos[state.pos[i]-1][self.move_on[i]]:
                    new_states.append(state.move(i, -1))
                # Regarder pour avancer (vers le haut)
                if state.pos[i] + self.length[i] < 6 and self.free_pos[state.pos[i] + self.length[i]][self.move_on[i]]:
                    new_states.append(state.move(i, 1))
        return new_states

    def solve(self, state):
        i = 0
        visited = set()
        fifo = deque([state])
        while len(fifo) > 0:
            current_state = fifo.popleft()
            i = i + 1

            if current_state not in visited:
                if current_state.success():
                    print(str(i) + " nombres d'états visités")
                    return current_state

                visited.add(current_state)
                new_states = self.possible_moves(current_state)
                for next_state in new_states:
                    if next_state not in visited:
                        fifo.append(next_state)
        return None

    def solve_Astar(self, state):
        i = 0
        visited = set()

        priority_queue = []
        state.h = state.estimee1()
        heapq.heappush(priority_queue, state)

        while len(priority_queue) > 0:
            current_state = heapq.heappop(priority_queue)
            i = i + 1
            if current_state not in visited:
                if current_state.success():
                    print(str(i) + " nombres d'états visités")
                    return current_state

                visited.add(current_state)
                new_states = self.possible_moves(current_state)
                for next_state in new_states:
                    if next_state not in visited:
                        heapq.heappush(priority_queue, next_state)
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