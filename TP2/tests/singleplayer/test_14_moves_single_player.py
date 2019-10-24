# solution optimale: 14 moves
from MiniMaxSearch import MiniMaxSearch
from Rushour import Rushhour
from State import State

rh = Rushhour([True, False, True, False, False, False, True, True, False, True, True],
                 [2, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2],
                 [2, 0, 0, 3, 4, 5, 3, 5, 2, 5, 4],
                 ["rouge", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
s = State([0, 0, 3, 1, 2, 1, 0, 0, 4, 3, 4])
algo = MiniMaxSearch(rh, s,1)
algo.rushhour.init_positions(s)
print(algo.rushhour.free_pos)
algo.solve(s, True)
%time
