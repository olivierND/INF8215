from Rushhour import Rushhour
from State import State


def solve16():
    rh = Rushhour([True, True, False, False, True, True, False, False],
                 [2, 2, 3, 2, 3, 2, 3, 3],
                 [2, 0, 0, 0, 5, 4, 5, 3],
                 ["rouge", "vert clair", "violet", "orange", "vert", "bleu ciel", "jaune", "bleu"])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    #s = rh.solve(s)
    s = rh.solve_Astar(s)
    n = rh.print_solution(s)


solve16()
print("\n--------------------------------------------\n")
# %time
