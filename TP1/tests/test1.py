from State import State


def test1():
    positioning = [1, 0, 1, 4, 2, 4, 0, 1]
    s0 = State(positioning)
    b = not s0.success()
    print(b)
    s = s0.move(1, 1)
    print(s.prev == s0)
    b = b and s.prev == s0
    print(s0.pos[1], " ", s.pos[1])
    s = s.move(6, 1)
    s = s.move(1, -1)
    s = s.move(6, -1)
    print(s == s0)
    b = b and s == s0
    s = s.move(1, 1)
    s = s.move(2, -1)
    s = s.move(3, -1)
    s = s.move(4, 1)
    s = s.move(4, -1)
    s = s.move(5, -1)
    s = s.move(5, 1)
    s = s.move(5, -1)
    s = s.move(6, 1)
    s = s.move(6, 1)
    s = s.move(6, 1)
    s = s.move(7, 1)
    s = s.move(7, 1)
    s = s.move(0, 1)
    s = s.move(0, 1)
    s = s.move(0, 1)
    print(s.success())
    b = b and s.success()
    print("\n", "résultat correct" if b else "mauvais résultat")


test1()
