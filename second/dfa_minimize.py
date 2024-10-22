import os
from collections import deque
import itertools


class DFA_State_Machine:
    def __init__(self, file=None):
        '''Constructing automat from the given file'''
        if file is None:
            self.m = 0
            self.n = 0
            self.start = 0
            self.is_end = [0]
            self.graph = []
            return

        with open(os.path.dirname(os.path.abspath(__file__)) + file, 'r') as f:
            self.n = int(f.readline())  # number of states
            self.m = int(f.readline())  # size of an alphabet

            self.start = int(f.readline())  # dfa has only one start
            self.is_end = [0 for i in range(self.n)]
            end = f.readline().split()
            for index in end:
                self.is_end[int(index)] = 1  # =1 if point is end, =0 otherwise

            self.graph = [[-1 for y in range(self.m)]
                          for x in range(self.n)]

            self.graph_to_from = [[-1 for y in range(self.n)]
                                  for x in range(self.n)]
            line = f.readline()
            while line:
                line = line.split()
                fr = int(line[0])
                way = int(line[1])
                to = int(line[2])
                # from state fr go to state to by elem = way
                self.graph[fr][way] = to
                # to state to get from state fr by elem = way
                self.graph_to_from[to][fr] = way
                line = f.readline()

    def dfs(self, v, word) -> bool:
        '''Check if it is possible
          to read given word in current machine'''
        if (len(word) == 0 and self.is_end[v] == 1):
            return True

        if (len(word) == 0 and self.is_end[v] == 0):
            return False

        char = int(word[0])
        if (self.graph[v][char] == -1):
            return False

        return self.dfs(self.graph[v][char], word[1::])

    def accept_word(self, word) -> bool:
        '''Start checking from all starting points'''
        return self.dfs(self.start, word)

    # add pairs of adjacent with i and j states
    def add_points(self, q, matrix, i, j):
        '''Add new elements to queue'''
        for a in range(self.n):
            for b in range(self.n):
                a_state = self.graph_to_from[i][a]
                b_state = self.graph_to_from[j][b]
                if (a_state != -1 and b_state != -1 and matrix[a][b] == -3):
                    matrix[a][b] = -2
                    matrix[b][a] = -2
                    q.append((a, b))
                a_state = self.graph_to_from[a][i]
                b_state = self.graph_to_from[b][j]
                if (a_state != -1 and b_state != -1 and matrix[a][b] == -3):
                    matrix[a][b] = -2
                    matrix[b][a] = -2
                    q.append((a, b))

    def dfa_minimize(self):
        '''Minimization algorithm'''
        # -3 - not used in q
        # -2 still are the same
        # -1 - diff as one final and other is not
        # matrix of differences between states
        matrix = [[-3]*self.n for i in range(self.n)]
        q = deque([])
        # add differences between final and non-final states
        for i in range(self.n):
            for j in range(i):
                if (self.is_end[i] != self.is_end[j]):
                    matrix[i][j] = -1  # diff if one final and other is not
                    matrix[j][i] = -1
                    self.add_points(q, matrix, i, j)

        while q:
            # get states that we check now
            first_state, second_state = q.popleft()
            for i in range(self.m):
                first_state_next = self.graph[first_state][i]
                second_state_next = self.graph[second_state][i]
                if (first_state_next == second_state_next):
                    continue
                if ((first_state_next == -1 and second_state_next != -1)
                    or (first_state_next != -1 and second_state_next == -1)):
                    # diff in this element
                    matrix[first_state][second_state] = i
                    matrix[second_state][first_state] = i
                    self.add_points(q, matrix, first_state, second_state)
                if (matrix[first_state_next][second_state_next] != -2):
                    # diff in this element
                    matrix[first_state][second_state] = i
                    matrix[second_state][first_state] = i
                    self.add_points(q, matrix, first_state, second_state)

        # add points, where both states are final and have no differences
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if (self.is_end[i] and self.is_end[j]
                        and matrix[i][j] == -3):
                        matrix[i][j] = -2
                        matrix[j][i] = -2

        self.build_new_minimized_machine(matrix)

    def build_new_minimized_machine(self, matrix):  # build new states and transitions
        '''Merge indefferent states and build
           new construction of machine'''
        used = [-1 for i in range(self.n)]
        new_start_state = 0
        new_end_states = []
        new_states_col = 0
        old_indexes_of_new_elements = []
        for i in range(self.n):
            if used[i] == -1:  # is not merged with anything else before
                new_index = new_states_col
                new_states_col += 1
                old_indexes_of_new_elements.append(i)
                used[i] = new_index
                if i == self.start:
                    new_start_state = new_index  # in dfa we have one start state, so here is also one start state
                if self.is_end[i]:
                    new_end_states.append(new_index)
                for j in range(i, self.n):
                    if matrix[i][j] == -2 or i == j:
                        used[j] = new_index

        new_graph = [[-1]*self.m for i in range(new_states_col)]
        for i in range(new_states_col):
            old_index = old_indexes_of_new_elements[i]
            for j in range(self.m):
                old_next_state = self.graph[old_index][j]
                if (old_next_state != -1):
                    new_index_for_old_one = used[old_next_state]
                new_graph[i][j] = new_index_for_old_one

        self.update(new_states_col, self.m, new_start_state, new_end_states, new_graph)

    def update(self, new_states_col, new_alphabet_size, new_start_state, new_end_states, new_graph):
        '''Update machine info'''
        self.n = new_states_col
        self.m = new_alphabet_size
        self.starts = new_start_state
        is_end = [0 for i in range(new_states_col)]
        for i in range(new_states_col):
            if i in new_end_states:
                is_end[i] = 1
        self.is_end = is_end
        self.graph = new_graph

    def check_equality(self, file=None) -> bool:
        '''Check if machine equals to the given in file
           or if file is not given then check that
           language contains all possibble words'''
        if (file is not None):  # if file is given - check with file
            other_machine = DFA_State_Machine(file)
        else:  # if not - check if machine contains all words
            other_machine = DFA_State_Machine()
            other_machine.n = 1
            other_machine.m = self.m
            other_machine.start = 0
            other_machine.is_end = [1]
            graph = [[0]*other_machine.m for i in range(other_machine.n)]
            other_machine.graph = graph

        other_machine.dfa_minimize()
        self.dfa_minimize()

        if (self.n != other_machine.n):
            return False

        if (self.m != other_machine.m):
            return False

        indexes = [i for i in range(other_machine.n)]
        all_permutations = list(itertools.permutations(indexes))
        flag = False
        for permutation in all_permutations:
            is_current_permutation = True
            for i in range(self.n):
                other_i = permutation[i]
                for j in range(self.m):
                    if (self.graph[i][j] != permutation[other_machine.graph[other_i][j]]):
                        is_current_permutation = False
                        break
                if is_current_permutation:
                    flag = True
                    break

        return flag

    def check_if_all_words(self):
        return self.check_equality()


# file format
# n - number of states
# m - size of alphabet
# ... - start points
# ... - end points
# from by to
