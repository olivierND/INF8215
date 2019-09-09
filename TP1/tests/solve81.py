from Rushhour import Rushhour
from State import State


def solve81():
    rh = Rushhour([True, False, True, False, False, False, False, True, False, False, True, True, True],
                 [2, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2],
                 [2, 0, 0, 4, 1, 2, 5, 3, 3, 2, 4, 5, 5],
                 ["rouge", "jaune", "vert clair", "orange", "bleu clair", "rose", "violet clair","bleu", "violet", "vert", "noir", "beige", "jaune clair"])
    s = State([3, 0, 1, 0, 1, 1, 1, 0, 3, 4, 4, 0, 3])
    s = rh.solve(s)
    #s = rh.solve_Astar(s)
    n = rh.print_solution(s)


solve81()
print("\n--------------------------------------------\n")
# %time
