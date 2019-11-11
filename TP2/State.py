import numpy as np
import math
import copy
from collections import deque


class State:
    """
    Contructeur d'un état initial
    """

    def __init__(self, pos):
        """
        pos donne la position de la voiture i dans sa ligne ou colonne (première case occupée par la voiture);
        """
        self.pos = np.array(pos)

        """
        c,d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None

        self.nb_moves = 0
        self.score = 0

        # TODO
        self.rock = None

        self.reasons = []

    """
    Constructeur d'un état à partir du mouvement (c,d)
    """

    def move(self, c, d):
        s = State(self.pos)
        s.prev = self
        s.pos[c] += d
        s.c = c
        s.d = d
        s.nb_moves = self.nb_moves + 1
        s.rock = self.rock
        return s

    def put_rock(self, rock_pos):
        s = State(self.pos)
        s.c = self.c
        s.d = self.d
        s.prev = self
        s.nb_moves = self.nb_moves
        s.rock = rock_pos
        return s

    def score_state(self, rh):
        score = 0
        if not self.success():
            rh.init_positions(self)
            car_size3 = 0
            columns_blocked = [0, 0, 0]
            score += 6 - self.pos[0]

            for car in range(1, rh.nbcars):
                if not rh.horiz[car]:
                    if rh.move_on[car] > self.pos[0]:
                        if self.pos[car] <= rh.move_on[0] < self.pos[car] + rh.length[car]:
                            if rh.length[car] == 3:
                                score += (3 - self.pos[car]) * 2
                                if rh.move_on[car] > 2:
                                    car_size3 += 1
                                    columns_blocked[rh.move_on[car] - 3] = 1
                            else:
                                score += 2
                                if self.pos[car] == 1 and not rh.free_pos[0][rh.move_on[car]] or\
                                   self.pos[car] == 2 and not rh.free_pos[4][rh.move_on[car]]:
                                    score += 3
                else:
                    if rh.length[car] == 3 and rh.move_on[car] < 2:
                        if (self.pos[car] + rh.length[car]) > (self.pos[0] + rh.length[0]):
                            nb_cases = (self.pos[car] + rh.length[car]) - (self.pos[0] + rh.length[0])
                            for i in range(nb_cases):
                                if not rh.free_pos[rh.move_on[car]][self.pos[car] - 1 - i]:
                                    score += 0.5
                            score += 0.25 * nb_cases

            if car_size3 > 0:
                if columns_blocked[0] == 1:
                    max_pos_3 = 0
                    max_pos_2 = 1
                elif columns_blocked[1] == 1:
                    max_pos_3 = 1
                    max_pos_2 = 2
                elif columns_blocked[2] == 1:
                    max_pos_3 = 2
                    max_pos_2 = 3
                else:
                    max_pos_3 = 0
                    max_pos_2 = 5
                for car in range(1, rh.nbcars):
                    if rh.horiz[car] and rh.move_on[car] > 2:
                        if rh.length[car] == 3 and self.pos[car] > max_pos_3:
                            score += (self.pos[car] - max_pos_3) * 4
                            for i in range(0, self.pos[car]):
                                if not rh.free_pos[rh.move_on[car]][i]:
                                    score += 5
                            for i in range(1, rh.nbcars):
                                if not rh.horiz[i] and rh.move_on[i] < 3:
                                    if self.pos[i] <= rh.move_on[car] <= self.pos[i] + rh.length[i]:
                                        if self.pos[i] + rh.length[i] > 5:
                                            if not rh.free_pos[self.pos[i] - 1][rh.move_on[i]]:
                                                score += 6
                                        elif self.pos[i] - 1 >= 0:
                                            if not rh.free_pos[self.pos[i] + rh.length[i]][rh.move_on[i]]:
                                                score += 6
                                        elif not rh.free_pos[self.pos[i] + rh.length[i]][rh.move_on[i]] \
                                                and not rh.free_pos[self.pos[i] - 1][rh.move_on[i]]:
                                            score += 6
                        elif rh.length[car] == 2 and self.pos[car] > max_pos_2:
                            score += (self.pos[car] - max_pos_2) * 4
                            for i in range(1, self.pos[car]):
                                if not rh.free_pos[rh.move_on[car]][i]:
                                    score += 5
                        elif rh.length[car] == 2 and max_pos_2 == 5:
                            if self.pos[car] == 2 or self.pos[car] == 3:
                                score += 4
        return score

    def success(self):
        return self.pos[0] == 4

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        if len(self.pos) != len(other.pos):
            print("les états n'ont pas le même nombre de voitures")

        return np.array_equal(self.pos, other.pos)

    def __hash__(self):
        h = 0
        for i in range(len(self.pos)):
            h = 37 * h + self.pos[i]
        return int(h)

    def __lt__(self, other):
        return self.score < other.score
