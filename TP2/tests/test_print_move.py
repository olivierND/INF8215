from MiniMaxSearch import MiniMaxSearch
from Rushour import Rushhour
from State import State


def test_print_move():
    rh = Rushhour([True], [2], [2], ["rouge"])
    s = State([0])
    s = s.put_rock((3,1)) # Roche dans la case 3-1
    s = s.move(0, 1) # Voiture rouge vers la droite

    algo = MiniMaxSearch(rh, s, 1)
    algo.print_move(True, s)
    algo.print_move(False, s)

test_print_move()