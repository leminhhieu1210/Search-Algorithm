from collections import defaultdict
from functools import reduce

FILE_IN = 'input/input_BFS_HCS.txt'
FILE_OUT = 'output/output_BFS_HCS.txt'
TABLE_WIDTH1 = 80
TABLE_WIDTH = 93

start, end = None, None
graph = defaultdict(list)
parent = {}
fist_value = 30


def f(node: tuple) -> str:  # (a,b) -> 'ba'
    return str(str(node[1]) + str(node[0]))


def format_queue(queue):  # [[a,b],[c]] -> [a,b,c]
    if len(queue) > 0:
        return reduce(lambda a, b: a + b, queue)
    return []


def print_path(st, ed, fi):
    if parent[ed] != st:
        print_path(st, parent[ed], fi)
    print(ed, end=' -> ', file=fi)


def make_graph():
    global start, end, graph
    with open(FILE_IN) as f:
        start, end = [str(x) for x in next(f).split()]
        for line in f:
            a, b, cost = [str(x) for x in line.split()]
            graph[a].append((int(cost), b))
        for key in graph:
            graph[key] = sorted(graph[key])


def BFS(st, ed):
    with open(FILE_OUT, 'w') as fi:
        print("%s %45s" % ("\n", "Best Fisrt Search"), file=fi)
        print("Quan he:", file=fi)
        print('-' * TABLE_WIDTH1, file=fi)
        print('| %-20s | %-20s | %-30s |' % ('Phat trien TT', 'Trang thai ke', 'Danh sach L'), file=fi)
        print('-' * TABLE_WIDTH1, file=fi)

        path = [(fist_value, st)]
        queue = [path.copy()]
        while queue:  # queue: [[(cost,to),()], [(),()],]
            path = queue.pop(0)  # path: [(),()]
            path_front = path.pop(0)  # path_front: (cost, to)

            if len(path) > 0:  # not insert [] to queue
                queue.insert(0, path)

            mid = 'TTKT - DUNG' if path_front[1] == ed else ', '.join(f(x) for x in graph[path_front[1]])
            next_path = []
            for _next in graph[path_front[1]]:
                parent[_next[1]] = path_front[1]
                next_path.append(_next)
            if len(next_path) > 0:
                queue.insert(0, next_path)
            queue = [sorted(format_queue(queue))]
            L = '' if path_front[1] == ed else ', '.join(f(x) for x in format_queue(queue))
            print('| %-20s | %-20s | %-30s |' % (f(path_front), mid, L), file=fi)

            if path_front[1] == ed:
                print('-' * TABLE_WIDTH1, file=fi)
                print("Duong di:", file=fi)
                print(st, end=' -> ', file=fi)
                print_path(st, ed, fi)
                return

        print('-' * TABLE_WIDTH1, file=fi)
        print("Khong di duoc", file=fi)


def hill_climbing_search(st, ed):
    with open(FILE_OUT, 'a') as fi:
        print("%s %55s" % ("\n", "Hill Climbing Search"), file=fi)
        print("Quan he:", file=fi)
        print('-' * TABLE_WIDTH, file=fi)
        print('| %-20s | %-20s | %-20s | %-20s |' % ('Phat trien TT', 'Trang thai ke', 'Danh sach L1', 'Danh sach L'), file=fi)
        print('-' * TABLE_WIDTH, file=fi)

        path = [(fist_value, st)]
        queue = [path.copy()]
        while queue:  # queue: [[(cost,to),()], [(),()],]
            path = queue.pop(0)  # path: [(),()]
            path_front = path.pop(0)  # path_front: (cost, to)

            if len(path) > 0:  # not insert [] to queue
                queue.insert(0, path)

            sort = sorted(graph[path_front[1]])
            mid = 'TTKT - DUNG' if path_front[1] == ed else ', '.join(f(x) for x in graph[path_front[1]])
            L1 = '' if path_front[1] == ed else ', '.join(f(x) for x in sort)
            L = '' if path_front[1] == ed else ', '.join(f(x) for x in (sort + format_queue(queue)))
            print('| %-20s | %-20s | %-20s | %-20s |' % (f(path_front), mid, L1, L), file=fi)

            if path_front[1] == ed:
                print('-' * TABLE_WIDTH, file=fi)
                print("Duong di:", file=fi)
                print(st, end=' -> ', file=fi)
                print_path(st, ed, fi)
                return

            next_path = []
            for _next in graph[path_front[1]]:
                parent[_next[1]] = path_front[1]
                next_path.append(_next)
            if len(next_path) > 0:
                queue.insert(0, next_path)

        print('-' * TABLE_WIDTH, file=fi)
        print("Khong di duoc", file=fi)


def remove_extra_character(path):
    my_file = open(path)
    content = my_file.read()[::-1].replace('>-', '', 1)  # remove last '->' in string
    content = content[::-1]
    with open(path, 'w') as fi:
        print(content, file=fi)


if __name__ == '__main__':
    make_graph()
    BFS(start, end)
    remove_extra_character(FILE_OUT)
    hill_climbing_search(start, end)
    remove_extra_character(FILE_OUT)