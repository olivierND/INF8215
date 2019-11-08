import numpy as np


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
        for i in range(self.nbcars):
            if self.horiz[i]:
                self.free_pos[self.move_on[i], state.pos[i]:state.pos[i] + self.length[i]] = False
            else:
                self.free_pos[state.pos[i]:state.pos[i] + self.length[i], self.move_on[i]] = False

        if state.rock is not None:
            self.free_pos[state.rock[0]][state.rock[1]] = False

    def possible_moves(self, state):
        self.init_positions(state)
        new_states = []
        for i in range(self.nbcars):
            if self.horiz[i]:
                if state.pos[i] + self.length[i] - 1 < 5 and self.free_pos[
                    self.move_on[i],
                    state.pos[i] + self.length[i]
                ]:
                    new_states.append(state.move(i, +1))
                if state.pos[i] > 0 and self.free_pos[self.move_on[i], state.pos[i] - 1]:
                    new_states.append(state.move(i, -1))
            else:
                if state.pos[i] + self.length[i] - 1 < 5 and self.free_pos[
                    state.pos[i] + self.length[i],
                    self.move_on[i]
                ]:
                    new_states.append(state.move(i, +1))
                if state.pos[i] > 0 and self.free_pos[state.pos[i] - 1, self.move_on[i]]:
                    new_states.append(state.move(i, -1))
        return new_states

    def possible_rock_moves(self, state):
        self.init_positions(state)
        new_states = []

        for i in range(6):
            for j in range(6):
                # S'il n'y a pas encore de rock,
                # on ne vérifie pas la condition pour la ligne/colonne de la roche précédente
                if state.rock is None and self.free_pos[i][j] and i != 2:
                    new_states.append(state.put_rock((i, j)))
                # Si on a une roche précédente, on vérifie sont numéro de ligne et colonne
                elif state.rock is not None and self.free_pos[i][j] and i != 2 and i != state.rock[0] and j != \
                        state.rock[1]:
                    new_states.append(state.put_rock((i, j)))

        return new_states

    def print_pretty_grid(self, state):
        self.init_positions(state)
        grid = np.chararray((6, 6))
        grid[:] = '-'
        for car in range(self.nbcars):
            for pos in range(state.pos[car], state.pos[car] + self.length[car]):
                if self.horiz[car]:
                    grid[self.move_on[car]][pos] = self.color[car][0]
                else:
                    grid[pos][self.move_on[car]] = self.color[car][0]
        grid[state.rock] = 'x'
        print(grid)
