from collections import defaultdict

FILE_IN = 'input_BrFS_DFS.txt'
FILE_OUT = 'output_BrFS_DFS.txt'
TABLE_WIDTH = 70

start, end = None, None
parent = {}
graph = defaultdict(list)


def print_path(st, ed, f):
    if parent[ed] != st:
        print_path(st, parent[ed], f)
    print(ed, end=' -> ', file=f)


def make_graph(path):
    global start, end, graph
    with open(path) as f:
        start, end = [str(x) for x in next(f).split()]
        for line in f:
            a, b = [str(x) for x in line.split()]
            graph[a].append(b)
    for key in graph:
        graph[key] = sorted(graph[key])


def BrFS(st, ed):
    with open(FILE_OUT, 'w') as f:
        print("%s %45s" % ("\n", "Breadth First Search"), file=f)
        print("Quan he:", file=f)
        print('-' * TABLE_WIDTH, file=f)
        print('| %-20s | %-20s | %-20s |' % ('Phat trien TT', 'Trang thai ke', 'Danh sach L'), file=f)
        print('-' * TABLE_WIDTH, file=f)

        queue = [st]
        visited = {}
        while queue:
            front = queue.pop(0)
            mid = 'TTKT - DUNG' if front == ed else ', '.join(str(x) for x in graph[front])
            print('| %-20s | %-20s | %-20s |' % (str(front), mid, ', '.join(str(x) for x in (queue + graph[front]))), file=f)

            if front == ed:
                print('-' * TABLE_WIDTH, file=f)
                print("Duong di:", file=f)
                print(st, end=" -> ", file=f)
                print_path(st, ed, f)
                return
            for i in graph[front]:
                if i not in visited:
                    visited[i] = 1
                    parent[i] = front
                    queue.append(i)

        print('\nKhong tim thay!', file=f)


def DFS(st, ed):
    with open(FILE_OUT, 'a') as f:
        print("%s %40s" % ("\n", "Depth First Search"), file=f)
        print("Quan he:", file=f)
        print('-' * TABLE_WIDTH, file=f)
        print('| %-20s | %-20s | %-20s |' % ('Phat trien TT', 'Trang thai ke', 'Danh sach L'), file=f)
        print('-' * TABLE_WIDTH, file=f)

        stack = [st]
        visited = {}
        while stack:
            top = stack.pop()
            mid = 'TTKT - DUNG' if top == ed else ', '.join(str(x) for x in graph[top])
            print('| %-20s | %-20s | %-20s |' % (str(top), mid, ' ,'.join(str(x) for x in (stack + graph[top]))[::-1]), file=f)

            if top == ed:
                print('-' * TABLE_WIDTH, file=f)
                print("Duong di:", file=f)
                print(st, end=" -> ", file=f)
                print_path(st, ed, f)
                return
            for i in graph[top]:
                if i not in visited:
                    visited[i] = 1
                    parent[i] = top
                    stack.append(i)

        print('\nKhong tim thay!', file=f)


def remove_extra_character(path):
    my_file = open(path)
    content = my_file.read()[::-1].replace('>-', '', 1)  # remove last '->' in string
    content = content[::-1]
    with open(path, 'w') as f:
        print(content, file=f)


if __name__ == '__main__':
    make_graph(FILE_IN)

    BrFS(start, end)
    remove_extra_character(FILE_OUT)

    DFS(start, end)
    remove_extra_character(FILE_OUT)
