import random

class MiniMaxSearch:
    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth
        self.visited = set()

    def minimax_1(self, current_depth, current_state):
        possible_moves = self.rushhour.possible_moves(current_state)

        if current_depth == self.search_depth:
            print("\n")
            print(str(current_state.reasons))
            print("score" + str(current_state.score))
            print(self.rushhour.free_pos)
            best_move = self.get_best_state(possible_moves)
            self.visited.add(best_move)
            best_move.score = best_move.score_state(self.rushhour)
            return best_move

        for s in possible_moves:
            best_move = self.minimax_1(current_depth + 1, s)

        return best_move

    def get_best_state(self, possible_moves):
        best_state = None
        for s in possible_moves:
            s.score = s.score_state(self.rushhour)

            # Enleve des points au states qui sont déjà visited
            if s in self.visited:
                s.reasons.append("Visited -3")
                s.score -= 3

            if best_state is None:
                best_state = s
            elif s.score > best_state.score:
                best_state = s

        return best_state

    def minimax_2(self, current_depth, current_state, is_max):
        if is_max:
            possible_moves = self.rushhour.possible_moves(current_state)
        else:
            possible_moves = self.rushhour.possible_rock_moves(current_state)

        if current_depth == self.search_depth:
            best_move = self.get_best_state(possible_moves)
            return best_move

        for s in possible_moves:
            best_move = self.minimax_1(current_depth + 1, s)

        return best_move

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        if current_depth == self.search_depth:
            best_move = self.get_best_state(possible_moves)
            return best_move

        if is_max:
            best_move = MIN
            possible_moves = self.rushhour.possible_moves(current_state)

            for s in possible_moves:
                child_best_move = self.minimax_1(current_depth + 1, s)
                best_move = max(child_best_move, best_move)
                alpha = max(alpha, best_move)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

        else:
            best_move = MAX
            possible_moves = self.rushhour.possible_rock_moves(current_state)

            for s in possible_moves:
                child_best_move = self.minimax_1(current_depth + 1, s)
                best_move = min(child_best_move, best_move)
                beta = min(beta, best_move)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

        return best_move

    def expectimax(self, current_depth, current_state, is_max):
        if is_max:
            possible_moves = self.rushhour.possible_moves(current_state)
        else:
            possible_moves = self.rushhour.possible_rock_moves(current_state)

        if current_depth == self.search_depth:
            best_move = random.choice(possible_moves)
            return best_move

        for s in possible_moves:
            best_move = self.minimax_1(current_depth + 1, s)

        return best_move

    def solve(self, state, is_singleplayer):
        if state.success():
            return state

        self.state = state
        if is_singleplayer:
            while not self.state.success():
                self.state = self.minimax_1(1, self.state)
            self.print_move(False, self.state)
        else:
            adversary = True
            while not self.state.success():
                adversary = not adversary
                self.minimax_2(0, state, adversary)

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
