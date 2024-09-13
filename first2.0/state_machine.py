import os


class State_Machine:
    def __init__(self, file):
        '''Constructing of an automat from the given file'''
        with open(os.path.dirname(os.path.abspath(__file__)) + file, 'r') as f:
            self.n = int(f.readline())  # number of states
            self.m = int(f.readline())  # size of an alphabet

            self.starts = [int(x) for x in f.readline().split()]
            self.ends = [0 for i in range(self.n)]
            end = f.readline().split()
            for index in end:
                self.ends[int(index)] = 1   # =1 if point is end, =0 otherwise

            self.graph = [[set() for y in range(self.m)]
                          for x in range(self.n)]
            line = f.readline()
            while line:
                line = line.split()
                fr = int(line[0])
                way = int(line[1])
                to = int(line[2])
                self.graph[fr][way].add(to)
                line = f.readline()
            self.new_point_to_index = dict()
            self.new_graph = []
            self.new_start_index = 0
            self.new_ends = []

    def dfs(self, v, word) -> bool:
        '''Check if it is possible
          to read given word in current machine'''
        if (len(word) == 0 and self.ends[v] == 1):
            return True

        if (len(word) == 0 and self.ends[v] == 0):
            return False

        char = int(word[0])
        if (len(self.graph[v][char]) == 0):
            return False

        for x in self.graph[v][char]:
            if(self.dfs(x, word[1::])):
                return True
        return False

    def accept_word(self, word) -> bool:
        '''Start checking from all starting points'''
        for start in self.starts:
            if (self.dfs(start, word)):
                return True
        return False
