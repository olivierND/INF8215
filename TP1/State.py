import numpy as np
import math
import copy


class State:
    """
    Contructeur d'un état initial
    """

    def __init__(self, pos):
        """
        pos donne la position de la voiture i (première case occupée par la voiture);
        """
        self.pos = np.array(pos)

        """
        c, d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None

        self.nb_moves = 0
        self.h = 0

    """
    Constructeur d'un état à partir mouvement (c,d)
    """

    def move(self, c, d):
        s = State(self.pos)
        s.c = c
        s.prev = self
        s.d = d
        s.nb_moves = self.nb_moves + 1
        s.pos[c] = s.pos[c] + d
        # s.h = s.estimee1()
        return s

    """ est il final? """

    def success(self):
        return self.pos[0] == 4

    """
    Estimation du nombre de coup restants 
    """

    def estimee1(self):
        return 4 - self.pos[0]

    def estimee2(self, rh):
        return self.estimee1() + self.get_cars_between_red_and_exit(rh)

    def get_cars_between_red_and_exit(self, rh):
        k = 0
        for i in range(len(self.pos)):
            if not rh.horiz[i] and rh.move_on[i] > self.pos[0] + 1:
                for j in range(rh.length[i]):
                    if self.pos[i] + j == 2:
                        k += 1
        return k

    # Pour cette heuristique, on vérifie pour chaque auto bloquant l'auto rouge, si elles sont aussi bloquées par
    # d'autres autos sur le jeu. Ainsi, on ajoute soit 1 au compteur si l'auto est bloquée par seulement une autre auto
    # par en haut ou par en bas, soit 2 au compteur si l'auto est bloquée des deux côtés et ne peut donc pas bouger.
    # Ceci nous permet de diminuer encore une fois le nombre d'états parcourus tout en trouvant la bonne solution.
    # La fonction estimee3 reprend l'estimée 1 et l'estimée 2 et nous ajoutons à celle-ci la fonction is_car_blocked(),
    # lorsqu'on trouve une voiture bloquant l'auto rouge.
    def estimee3(self, rh):
        k = 0
        for i in range(len(self.pos)):
            if not rh.horiz[i] and rh.move_on[i] > self.pos[0] + 1:
                for j in range(rh.length[i]):
                    if self.pos[i] + j == 2:
                        d = self.is_car_blocked(rh, i)
                        k += 1 + d
        return self.estimee1() + k

    # Fonction qui vérifie si l'auto bloquante est elle-même bloquée par 1 ou 2 autos en verticale ou en horizontale.
    def is_car_blocked(self, rh, car_index):
        k = 0
        for i in range(len(self.pos)):
            if rh.horiz[i]:
                if rh.move_on[i] == self.pos[car_index] + rh.length[car_index]:
                    k += 1
                if rh.move_on[i] == self.pos[car_index] - 1:
                    k += 1
            else:
                if rh.move_on[car_index] == rh.move_on[i]:
                    if self.pos[i] == self.pos[car_index] + rh.length[car_index]:
                        k += 1
                    if self.pos[i] + rh.length[car_index] - 1 == self.pos[car_index] - 1:
                        k += 1
        return k

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
        return (self.nb_moves + self.h) < (other.nb_moves + other.h)