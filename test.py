TABLE_WIDTH = 177

class Graph:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        # if not self.directed:
        #     self.graph_dict.setdefault(B, {})[A] = distance

    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))


# A* search
def astar_search(graph, heuristics, start, end):
    print("%s %55s" % ("\n", "A Star Search"))
    print("Quan he:")
    print('-' * TABLE_WIDTH)
    print('| %-20s | %-20s | %-20s | %-20s | %-20s | %-20s | %-35s |' % ('TT', 'TTK', 'k(u, v)', 'h(v)', 'g(v)', 'f(v)', 'Danh sach L'))
    print('-' * TABLE_WIDTH)


    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)

    # Loop until the open list is empty
    while len(open) > 0:
        check = 0

        # Sort the open list to get the node with the lowest cost first
        open.sort()

        # Get the node with the lowest cost
        current_node = open.pop(0)
        # print("TT = ", current_node.name)
        s = '| %-20s ' % (current_node.name)
        print(s, end='')
        # Add the current node to the closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
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
            # result = path[::-1]
            result += start_node.name + ", do dai = " + str(distance)
            # Return reversed path
            return result
        # Get neighbours
        neighbors = graph.get(current_node.name)

        # Loop neighbors
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = Node(key, current_node)
            # Check if the neighbor is in the closed list
            if (neighbor in closed):
                continue
            # Calculate full path cost
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # print("kc = ", graph.get(current_node.name, neighbor.name))
            # print(neighbor.name, neighbor.h, neighbor.g, neighbor.f)

            _ttk = neighbor.name
            _k = graph.get(current_node.name, neighbor.name)
            _h = neighbor.h
            _g = neighbor.g
            _f = neighbor.f

            if check == 0:
                print('| %-20s | %-20s | %-20s | %-20s | %-20s | %-35s |' % (_ttk, _k, _h, _g, _f, ""))
                check = 1
            else:
                print('| %-20s | %-20s | %-20s | %-20s | %-20s | %-20s | %-35s |' % ("", _ttk, _k, _h, _g, _f, ""))

            # Check if neighbor is in open list and if it has a lower f value
            if (add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)

        # print("open = ", open, '\n')
        open.sort()
        _o = [str(i.name + str(i.f)) for i in open]
        print('| %-20s | %-20s | %-20s | %-20s | %-20s | %-20s | %-35s |' % ("", "", "", "", "", "", ', '.join(elem for elem in _o)))
        print('-' * TABLE_WIDTH)

    # Return None, no path is found
    return None


# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True


# The main entry point for this module
def main():
    # Create a graph
    graph = Graph()
    # Create graph connections (Actual distance)
    graph.connect('A', 'C', 9)
    graph.connect('A', 'D', 7)
    graph.connect('A', 'E', 13)
    graph.connect('A', 'F', 20)
    graph.connect('C', 'H', 6)
    graph.connect('D', 'E', 4)
    graph.connect('D', 'H', 8)
    graph.connect('E', 'K', 4)
    graph.connect('E', 'I', 3)
    graph.connect('F', 'G', 4)
    graph.connect('F', 'I', 6)
    graph.connect('H', 'K', 5)
    graph.connect('I', 'K', 9)
    graph.connect('I', 'B', 5)
    graph.connect('K', 'B', 6)

    # Make graph undirected, create symmetric connections
    graph.make_undirected()
    # Create heuristics (straight-line distance, air-travel distance)
    heuristics = {}
    heuristics['A'] = 14
    heuristics['B'] = 0
    heuristics['C'] = 15
    heuristics['D'] = 6
    heuristics['E'] = 8
    heuristics['F'] = 7
    heuristics['G'] = 12
    heuristics['H'] = 10
    heuristics['I'] = 4
    heuristics['K'] = 2

    # Run the search algorithm
    path = astar_search(graph, heuristics, 'A', 'B')
    print('| %-35s %97s' % (path, "|"))
    print('-' * TABLE_WIDTH)


# Tell python to run main method
if __name__ == "__main__":
    main()