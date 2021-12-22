TABLE_WIDTH = 117
FILE_IN = 'input/input_Astar.txt'
FILE_OUT = 'output/output_Astar.txt'

class Graph:
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


class Node:
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        if self.f < other.f:
            return True
        if self.f == other.f:
            return self.name < other.name
        return self.f < other.f

    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))


def astar_search(graph, weights, start, end):
    with open(FILE_OUT, 'w') as fi:
        print("%s %60s" % ("\n", "A Star Search"), file=fi)
        print("Quan he:", file=fi)
        print('-' * TABLE_WIDTH, file=fi)
        print('| %-10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-35s |' % ('TT', 'TTK', 'k(u, v)', 'h(v)', 'g(v)', 'f(v)', 'Danh sach L'), file=fi)
        print('-' * TABLE_WIDTH, file=fi)

        list_open = []
        list_closed = []

        start_node = Node(start, None)
        goal_node = Node(end, None)

        list_open.append(start_node)

        while len(list_open) > 0:
            check = 0
            list_open.sort()

            current_node = list_open.pop(0)
            s = '| %-10s ' % (current_node.name)
            print(s, end='', file=fi)
            list_closed.append(current_node)

            if current_node == goal_node:
                path = []
                distance = 0
                check2 = 0
                result = "TTKT/dung, duong di "

                while current_node != start_node:
                    if check2 == 0:
                        distance = current_node.g
                        check2 = 1
                    path.append(current_node.name + ': ' + str(current_node.g))
                    result += current_node.name + ' <- '
                    current_node = current_node.parent
                path.append(start_node.name + ': ' + str(start_node.g))
                result += start_node.name + ", do dai = " + str(distance)

                return result

            neighbors = graph.get(current_node.name)
            print(current_node , neighbors)
            for key, value in neighbors.items():
                neighbor = Node(key, current_node)
                # if (neighbor in list_closed):
                #     continue
                neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
                neighbor.h = weights.get(neighbor.name)
                neighbor.f = neighbor.g + neighbor.h

                _ttk = neighbor.name
                _k = graph.get(current_node.name, neighbor.name)
                _h = neighbor.h
                _g = neighbor.g
                _f = neighbor.f

                if check == 0:
                    print('| %-10s | %-10s | %-10s | %-10s | %-10s | %-35s |' % (_ttk, _k, _h, _g, _f, ""), file=fi)
                    check = 1
                else:
                    print('| %-10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-35s |' % ("", _ttk, _k, _h, _g, _f, ""), file=fi)

                if (add_to_open(list_open, neighbor) == True):
                    list_open.append(neighbor)

            list_open.sort()
            _open = [str(i.name + str(i.f)) for i in list_open]
            print('| %-10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-35s |' % ("", "", "", "", "", "", ', '.join(elem for elem in _open)), file=fi)
            print('-' * TABLE_WIDTH, file=fi)

        return None


def add_to_open(list_open, neighbor):
    for node in list_open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True


def main():
    graph = Graph()
    weights = {}

    with open(FILE_IN) as f:
        start, end = [str(x) for x in next(f).split()]
        for line in f:
            a, w_a, b, w_b, cost = line.split()
            graph.connect(a, b, int(cost))
            weights[a] = int(w_a)
            weights[b] = int(w_b)

            # if len(line.split()) == 3:
            #     a, b, cost = [str(x) for x in line.split()]
            #     graph.connect(a, b, int(cost))
            # elif len(line.split()) == 2:
            #     a, w = [str(x) for x in line.split()]
            #     weights[a] = int(w)

    # graph.make_undirected()

    path = astar_search(graph, weights, start, end)
    with open(FILE_OUT, 'a') as fi:
        print('| %-35s %47s' % (path, "|"), file=fi)
        print('-' * TABLE_WIDTH, file=fi)


if __name__ == "__main__":
    main()