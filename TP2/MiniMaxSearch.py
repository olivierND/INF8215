import random
import numpy
from enum import Enum


class Expectimax(Enum):
    Random = 0,
    Optimistic = 1,
    Pessimistic = 2


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
            return current_state

        if is_max:
            possible_moves = self.rushhour.possible_rock_moves(current_state)
            score = float('-inf')
        else:
            possible_moves = self.rushhour.possible_moves(current_state)
            score = float('inf')

        possible_states = []

        for s in possible_moves:
            if s.success() and current_depth != self.search_depth:
                return s

            state = self.minimax_2(current_depth + 1, s, not is_max)
            state.score = state.score_state(self.rushhour)

            if is_max and state.score >= score:
                if state.score > score:
                    possible_states.clear()
                score = state.score
                s.score = score
                possible_states.append(s)

            elif not is_max and state.score <= score:
                if state.score < score:
                    possible_states.clear()
                score = state.score
                s.score = score
                possible_states.append(s)

        return random.choice(possible_states)

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        if current_depth == self.search_depth:
            return current_state

        if is_max:
            possible_moves = self.rushhour.possible_rock_moves(current_state)
            score = float('-inf')
        else:
            possible_moves = self.rushhour.possible_moves(current_state)
            score = float('inf')

        possible_states = []

        for s in possible_moves:
            if s.success() and current_depth != self.search_depth:
                return s

            state = self.minimax_pruning(current_depth + 1, s, not is_max, alpha, beta)
            state.score = state.score_state(self.rushhour)

            if is_max:
                alpha = max(alpha, state.score)

                if state.score >= score:
                    if state.score > score:
                        possible_states.clear()
                    score = state.score
                    s.score = score
                    possible_states.append(s)

                if score >= beta:
                    s.score = score
                    return s
            else:
                beta = max(beta, state.score)

                if state.score <= score:
                    if state.score < score:
                        possible_states.clear()
                    score = state.score
                    s.score = score
                    possible_states.append(s)

                if alpha >= score:
                    s.score = score
                    return s

        return random.choice(possible_states)

    def expectimax(self, current_depth, current_state, is_max, mode):
        if current_depth == self.search_depth:
            return current_state

        if is_max:
            possible_moves = self.rushhour.possible_rock_moves(current_state)
            score = float('-inf')
        else:
            possible_moves = self.rushhour.possible_moves(current_state)
            score = float('inf')

        possible_states = []
        possible_states_probability = []
        total_score = 0

        for s in possible_moves:
            if s.success() and current_depth != self.search_depth:
                return s

            state = self.expectimax(current_depth + 1, s, not is_max, mode)
            state.score = state.score_state(self.rushhour)

            if is_max:
                s.score = state.score
                possible_states.append(s)
                total_score += state.score

            elif not is_max and state.score <= score:
                if state.score < score:
                    possible_states.clear()
                score = state.score
                s.score = score
                possible_states.append(s)

        if is_max:
            if mode == Expectimax.Random or total_score == 0:
                return random.choice(possible_states)

            elif mode == Expectimax.Pessimistic:
                for state in possible_states:
                    possible_states_probability.append(state.score / total_score)
                return numpy.random.choice(possible_states, p=possible_states_probability)

            elif mode == Expectimax.Optimistic:
                possible_states.sort(key=lambda x: x.score)
                for state in possible_states:
                    possible_states_probability.append(state.score / total_score)
                return numpy.random.choice(possible_states, p=possible_states_probability.reverse())

        else:
            return random.choice(possible_states)

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
