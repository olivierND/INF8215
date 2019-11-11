import random
import numpy as np

class MiniMaxSearch:
    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth

    def minimax_1(self, current_depth, current_state):
        if current_depth == self.search_depth:
            current_state.score = current_state.score_state(self.rushhour)
            return current_state

        min_score = float('inf')
        possible_moves = self.rushhour.possible_moves(current_state)
        possible_states = []

        for s in possible_moves:
            if s.success() and current_depth != self.search_depth:
                return s
            state = self.minimax_1(current_depth + 1, s)

            if state.score <= min_score:
                min_score = state.score
                s.score = min_score
                possible_states.append(s)

        return random.choice([s for s in possible_states if s.score == min_score])

    def minimax_2(self, current_depth, current_state, is_max):
        if current_depth == self.search_depth:
            current_state.score = current_state.score_state(self.rushhour)
            return current_state

        score = float('-inf') if is_max else float('inf')
        possible_states = []
        possible_moves = self.rushhour.possible_rock_moves(current_state) if is_max else self.rushhour.possible_moves(
            current_state)

        for s in possible_moves:
            if s.success() and current_depth != self.search_depth:
                return s

            state = self.minimax_2(current_depth + 1, s, not is_max)
            if is_max:
                if state.score >= score:
                    score = state.score
                    s.score = score
                    possible_states.append(s)
            else:
                if state.score <= score:
                    score = state.score
                    s.score = score
                    possible_states.append(s)

        return random.choice([s for s in possible_states if s.score == score])

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        if current_depth == self.search_depth:
            current_state.score = current_state.score_state(self.rushhour)
            return current_state

        score = float('-inf') if is_max else float('inf')
        possible_states = []
        possible_moves = self.rushhour.possible_rock_moves(current_state) if is_max else self.rushhour.possible_moves(
            current_state)

        for s in possible_moves:
            if s.success() and current_depth != self.search_depth:
                return s

            state = self.minimax_pruning(current_depth + 1, s, not is_max, alpha, beta)
            if is_max:
                if state.score >= score:
                    score = state.score
                    s.score = score
                    possible_states.append(s)
                if score >= beta:
                    s.score = score
                    return s
                alpha = max(alpha, state.score)
            else:
                if state.score <= score:
                    score = state.score
                    s.score = score
                    possible_states.append(s)
                if alpha >= score:
                    s.score = score
                    return s
                beta = max(beta, state.score)

        return random.choice([s for s in possible_states if s.score == score])

    def solve(self, state, is_singleplayer, is_pruning):
        if state.success():
            return state

        adversary = False
        if is_singleplayer:
            while not self.state.success():
                self.state = self.minimax_1(0, self.state)
            self.print_move(self.state)
        else:
            while not self.state.success():
                if is_pruning:
                    self.state = self.minimax_pruning(0, self.state, adversary, float('-inf'), float('inf'))
                else:
                    self.state = self.minimax_2(0, self.state, adversary)
            self.print_move(self.state)
        return None

    def print_move(self, state):
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
