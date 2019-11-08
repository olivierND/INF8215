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
        # TODO
        return s

    def put_rock(self, rock_pos):
        # TODO
        s = State(self.pos)
        s.prev = self

        s.rock = rock_pos
        return s

    def score_state(self, rh):
        score = self.pos[0] * 10

        if self.success():
            score = 1000

        for car in range(rh.nbcars):
            # Si la voiture est verticale et devant la voiture rouge
            if not rh.horiz[car] and rh.move_on[car] >= self.pos[0] + 1:
                # Si la voiture bloque la voiture rouge (index 0)
                if self.is_car_blocked(rh, 0, car):
                    facteur = 10
                    compteur = 0
                    # Si la premiere voiture est bloquee par une deuxieme voiture
                    for car2 in range(rh.nbcars):
                        if self.is_car_blocked(rh, car, car2) and car != car2:
                            # Si la voiture est bloquee, on augmente son facteur
                            facteur = 100
                            compteur += 1

                            # Si la deuxieme voiture est bloquee par des voitures
                            compteur2 = 0
                            for car3 in range(rh.nbcars):
                                if self.is_car_blocked(rh, car2, car3) and car2 != car3:
                                    # Si la deuxieme voiture est bloquee, on augmente son facteur
                                    facteur = 1000

                        # Si la roche bloque cette voiture
                        if self.rock and self.rock[1] == rh.move_on[car]:
                            score -= facteur
                        # On penalise moins car la voiture bloquante n'est pas elle-meme bloquee
                        elif compteur == 0:
                            score -= facteur
                        # On penalise les voitures bloquantes par le nombre de voitures qui la bloque elle-meme
                        elif compteur > 0:
                            score -= compteur * facteur

        return score

    def is_car_blocked(self, rh, blocked_car, car):
        # Si les voitures sont horizontales et sur la meme ligne
        if rh.horiz[car] == rh.horiz[blocked_car] and rh.move_on[car] == rh.move_on[blocked_car]:
            return True;

        # Si la voiture bloquante est verticale, bloque-t-elle la voiture rouge?
        if rh.horiz[car] != rh.horiz[blocked_car]:
            return self.pos[car] <= rh.move_on[blocked_car] < self.pos[car] + rh.length[car]
        return False

    def is_closer_to_exit(self):
        return self.prev is not None and self.pos[0] > self.prev.pos[0]

    def is_further_to_exit(self):
        return self.prev is not None and self.pos[0] < self.prev.pos[0]

    def is_current_in_red_cars_way(self, rh, i):
        if not rh.horiz[i] and rh.move_on[i] > self.pos[0] + 1:
            for j in range(rh.length[i]):
                if self.pos[i] + j == 2:
                    return True
        return False

    def is_previous_in_red_cars_way(self, rh, i):
        if self.prev is not None and not rh.horiz[i] and rh.move_on[i] > self.prev.pos[0] + 1:
            for j in range(rh.length[i]):
                if self.prev is not None and self.prev.pos[i] + j == 2:
                    return True
        return False

    def is_truck_getting_out_of_red_cars_way(self, rh, i):
        return self.prev is not None and not rh.horiz[i] and rh.move_on[i] > self.pos[0] + 1 \
               and rh.length[i] == 3 and self.pos[i] > self.prev.pos[i]

    def is_truck_getting_in_red_cars_way(self, rh, i):
        return self.prev is not None and not rh.horiz[i] and rh.move_on[i] > self.pos[0] + 1 \
               and rh.length[i] == 3 and self.pos[i] < self.prev.pos[i]

    def current_blocks_car_thats_in_red_cars_way(self, rh, i):
        if self.is_current_in_red_cars_way(rh, i):
            for j in range(len(self.pos)):
                if rh.horiz[j]:
                    if rh.move_on[j] == self.pos[i] + rh.length[i]:
                        for k in range(rh.length[j]):
                            if self.pos[j] + k == rh.move_on[i]:
                                return True

                    if rh.move_on[j] == self.pos[i] - 1:
                        for k in range(rh.length[j]):
                            if self.pos[j] + k == rh.move_on[i]:
                                return True
        return False

    def previous_blocks_car_thats_in_red_cars_way(self, rh, i):
        if self.is_previous_in_red_cars_way(rh, i):
            for j in range(len(self.prev.pos)):
                if rh.horiz[j]:
                    if rh.move_on[j] == self.prev.pos[i] + rh.length[i]:
                        for k in range(rh.length[j]):
                            if self.prev.pos[j] + k == rh.move_on[i]:
                                return True

                    if rh.move_on[j] == self.prev.pos[i] - 1:
                        for k in range(rh.length[j]):
                            if self.prev.pos[j] + k == rh.move_on[i]:
                                return True

        return False

    # Fonction qui vérifie si l'auto bloquante est elle-même bloquée par 1 ou 2 autos ou roche en verticale
    # ou en horizontale.
    # def is_car_blocked_by_car(self, rh, car_index):
    #     k = 0
    #     for i in range(len(self.pos)):
    #         if rh.horiz[i]:
    #             if rh.move_on[i] == self.pos[car_index] + rh.length[car_index]:
    #                 k -= 1
    #             if rh.move_on[i] == self.pos[car_index] - 1:
    #                 k -= 1
    #         else:
    #             if rh.move_on[car_index] == rh.move_on[i]:
    #                 if self.pos[i] == self.pos[car_index] + rh.length[car_index]:
    #                     k -= 1
    #                 if self.pos[i] + rh.length[car_index] - 1 == self.pos[car_index] - 1:
    #                     k -= 1
    #     return k + self.is_car_blocked_by_rock(rh, car_index)

    def is_car_blocked_by_rock(self, rh, car_index):
        if self.rock is None:
            return 0

        k = 0

        if rh.horiz[car_index]:
            # La roche est en arriere ou en avant de l'auto
            if (self.rock[0] == rh.move_on[car_index] and self.rock[1] == self.pos[car_index] - 1) \
                    or (self.rock[0] == rh.move_on[car_index] and self.rock[1] == self.pos[car_index] + rh.length[
                car_index]):
                k -= 1
        else:
            # La roche est a gauche ou a droite de l'auto
            if (self.rock[1] == rh.move_on[car_index] and self.rock[0] == self.pos[car_index] - 1) \
                    or (self.rock[1] == rh.move_on[car_index] and self.rock[0] == self.pos[car_index] + rh.length[
                car_index]):
                k -= 1
        if k == 0:
            return 1

        return k

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
        return (self.score) < (other.score)
