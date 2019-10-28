from collections import deque


class MiniMaxSearch:
    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth

    def minimax_1(self, current_depth, current_state):
        # TODO
        possible_moves = self.rushhour.possible_moves(current_state)

        if current_depth == self.search_depth:
            best_move = self.get_best_state(possible_moves)
            return best_move

        for s in possible_moves:
            best_move = self.minimax_1(current_depth + 1, s)

        return best_move

    def get_best_state(self, possible_moves):
        best_state = None
        for s in possible_moves:
            s.score = s.score_state(self.rushhour)
            if best_state is None:
                best_state = s
            elif s.score > best_state.score:
                best_state = s

        return best_state

    # def minimax_2(self, current_depth, current_state, is_max):
    #     # TODO
    #     return best_move
    #
    # def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
    #     # TODO
    #     return best_move
    #
    # def expectimax(self, current_depth, current_state, is_max):
    #     # TODO
    #     return best_move
    #
    # def decide_best_move_1(self):
    #     # TODO
    #
    # def decide_best_move_2(self, is_max):
    #
    # # TODO
    #
    # def decide_best_move_pruning(self, is_max):
    #
    # # TODO
    #
    # def decide_best_move_expectimax(self, is_max):
    #
    # # TODO

    def solve(self, state, is_singleplayer):
        if state.success():
            return state

        self.state = state
        if is_singleplayer:
            while not self.state.success():
                self.state = self.minimax_1(1, self.state)
            self.print_move(False, self.state)
        else:
            self.minimax_2(0, state, False)


    # TODO

    def print_move(self, is_max, state):
        i = 1
        while state.prev is not None:
            output = str(i) + ". Voiture " + self.rushhour.color[state.c] + " vers "
            if self.rushhour.horiz[state.c]:
                if state.d > 0:
                    output += "la gauche."
                else:
                    output += "la droite."
            else:
                if state.d > 0:
                    output += "le bas."
                else:
                    output += "le haut."

            print(output)
            i += 1
            state = state.prev
        return 0
