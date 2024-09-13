import os

class Converter:
    def __init__(self, file):
        '''Constructing of an automat from the given file'''
        with open(os.path.dirname(os.path.abspath(__file__)) + file, 'r') as f:
            self.n = int(f.readline()) # number of states
            self.m = int(f.readline()) # size of an alphabet

            self.starts = set(int(x) for x in f.readline().split()) # start points
            self.ends = [0 for i in range(self.n)] 
            end = f.readline().split()
            for index in end:
                self.ends[int(index)] = 1  # = 1 if point is end, = 0 otherwise

            self.graph = [[set() for y in range(self.m)] for x in range(self.n)] 
            line = f.readline()
            while line:
                line = line.split()
                fr = int(line[0])
                way = int(line[1])
                to = int(line[2])
                self.graph[fr][way].add(to)
                line = f.readline()
            self.new_points = []
            self.new_graph = []
            self.new_ends = set()

    def dfs(self, point):
        '''Функция конвертации NFA в DFA с помощью трансформированного dfs'''
        self.new_points.append(point)
        # for elem in self.new_points:
        #     print(elem)
        # print('ha')
        self.new_graph.append([[] for i in range (self.m)])
        index = len(self.new_points) - 1
        # print(index)
        for i in range(self.m):
            new_point = set() # set состояний, в который можем перейти из этой точки по данному символу
            for elem in point:
                if (self.ends[elem]):
                    self.new_ends.add(index) # если одна из объединенных точек была конечной, то новая точка тоже конечная
                for el in self.graph[elem][i]:
                    new_point.add(el)

            if (new_point): #проверяем, была ли раньше такая непустая точка и добавляем при отсутсвие, 
                # рекурсивно запуская из нее тот же алгоритм объединения
                # if new_point not in self.new_points:
                #     print('hey', new_point)
                #     self.dfs(new_point)
                # for elem in self.new_points:
                #     if ():
                #         self.dfs(new_point)
                #         break
                new = True
                for elem in self.new_points:
                    if elem == new_point:
                        new = False
                        break
                if(new):
                    self.dfs(new_point)
                new_point_index = self.new_points.index(new_point)
                # print(index, point, i, new_point, new_point_index)
                self.new_graph[index][i].append(new_point_index) # добавляем переход в новую точку

    def print_new_dfa(self, file):
         with open(os.path.dirname(os.path.abspath(__file__)) + file, 'w') as f:
            f.write(str(len(self.new_points)) + '\n')
            f.write(str(self.m) + '\n')
            f.write('0\n')
            f.write(' '.join(map(str, self.new_ends)) + '\n')
            for i in range(len(self.new_graph)):
                for j in range(self.m):
                    if (not self.new_graph[i][j]): continue
                    f.write(str(i) + ' ' + str(j) + ' ' + str(self.new_graph[i][j][0]) + ' ' +'\n')

    def make_dfa(self, file):
        self.dfs(self.starts)
        self.print_new_dfa(file)

    def check_correctness(self):
        pass



