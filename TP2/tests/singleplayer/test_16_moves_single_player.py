# solution optimale: 16 moves
from MiniMaxSearch import MiniMaxSearch
from Rushour import Rushhour
from State import State

rh = Rushhour([True, True, False, False, True, True, False, False],
                 [2, 2, 3, 2, 3, 2, 3, 3],
                 [2, 0, 0, 0, 5, 4, 5, 3],
                 ["rouge", "vert", "mauve", "orange", "emeraude", "lime", "jaune", "bleu"])
s = State([1, 0, 1, 4, 2, 4, 0, 1])
algo = MiniMaxSearch(rh, s, 1)
algo.rushhour.init_positions(s)
print(algo.rushhour.free_pos)
algo.solve(s, True, False, False)