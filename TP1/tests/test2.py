from Rushhour import Rushhour
from State import State


def test2():
    rh = Rushhour([True, True, False, False, True, True, False, False],
                  [2, 2, 3, 2, 3, 2, 3, 3],
                  [2, 0, 0, 0, 5, 4, 5, 3])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    rh.init_positions(s)
    b = True
    print(rh.free_pos)
    ans = [[False, False, True, True, True, False], [False, True, True, False, True, False],
           [False, False, False, False, True, False],
           [False, True, True, False, True, True], [False, True, True, True, False, False],
           [False, True, False, False, False, True]]
    b = b and (rh.free_pos[i, j] == ans[i, j] for i in range(6) for j in range(6))
    print("\n", "résultat correct" if b else "mauvais résultat")


test2()
