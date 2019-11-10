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
            best_move = self.max(possible_moves)
            self.visited.add(best_move)
            best_move.score = best_move.score_state(self.rushhour)
            return best_move

        for s in possible_moves:
            best_move = self.minimax_1(current_depth + 1, s)

        return best_move

    def max(self, possible_moves):
        max_state = None
        for s in possible_moves:
            s.score = s.score_state(self.rushhour)

            # Enleve des points au states qui sont déjà visited
            if s in self.visited:
                s.reasons.append("Visited -3")
                s.score -= 3

            if max_state is None:
                max_state = s
            elif s.score > max_state.score:
                max_state = s

        return max_state

    def min(self, possible_moves):
        min_state = None
        for s in possible_moves:
            s.score = s.score_state(self.rushhour)

            # Enleve des points au states qui sont déjà visited
            if s in self.visited:
                s.reasons.append("Visited -3")
                s.score -= 3

            if min_state is None:
                min_state = s
            elif s.score < min_state.score:
                min_state = s

        return min_state

    def minimax_2(self, current_depth, current_state, is_max):
        # Lorsqu'on atteint notre search_depth on retourne le state
        if current_depth == self.search_depth:
            return current_state

        if is_max:
            # Coups possibles pour la roche
            possible_moves = self.rushhour.possible_rock_moves(current_state)
        else:
            # Coups possibles pour les autos
            possible_moves = self.rushhour.possible_moves(current_state)

        search_depth_moves = []
        # On rappel Minimax2 jusqu'à notre search_depth
        for s in possible_moves:
            # Retourne le state si success
            if s.success():
                return s

            move = self.minimax_2(current_depth + 1, s, not is_max)
            # On append tout les noeuds qui sont au search depth
            search_depth_moves.append(move)

        # On choisit le noeud ayant le meilleur ou pire score selon is_max
        if is_max:
            move = self.max(search_depth_moves)
        else:
            move = self.min(search_depth_moves)

        return move

    def decide_best_move_2(self, is_max):
        self.state = self.minimax_2(1, self.state, is_max)
        self.rushhour.init_positions(self.state)
        print("\n")
        print(self.rushhour.free_pos)

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        if current_depth == self.search_depth:
            best_move = self.max(possible_moves)
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
            adversary = False
            while not self.state.success():
                self.decide_best_move_2(adversary)
                adversary = not adversary

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
