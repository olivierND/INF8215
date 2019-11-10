# Solution optimale: 9 moves
from MiniMaxSearch import MiniMaxSearch
from Rushour import Rushhour
from State import State

rh = Rushhour([True, False, False, False, True],
                 [2, 3, 2, 3, 3],
                 [2, 4, 5, 1, 5],
                 ["rouge", "vert", "bleu", "orange", "jaune"])
s = State([1, 0, 1, 3, 2])
algo = MiniMaxSearch(rh, s,3)
algo.rushhour.init_positions(s)
print(algo.rushhour.free_pos)
algo.solve(s, False)
