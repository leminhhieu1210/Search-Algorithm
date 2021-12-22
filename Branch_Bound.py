from collections import defaultdict
from functools import reduce

FILE_IN = 'input_BranchBound.txt'
FILE_OUT = 'output_BranchBound.txt'
TABLE_WIDTH = 155

start = None
end = None

graph = defaultdict(list)
count = 0
k = {}
h = {}
g = {}
f = {}

parent = {}


def fm(node: tuple) -> str:  # (a,b) -> ba
    return str(str(node[1]) + '_' + str(node[0]))


def format_queue(queue):  # [[],[]] -> []
    if len(queue) > 0:
        return reduce(lambda a, b: a + b, queue)
    return []


def make_graph():
    global start, end, graph, k, h, g, f, count
    with open(FILE_IN) as fi:
        # start, w_st, end, w_ed = [str(x) for x in next(fi).split()]

        start, end = [str(x) for x in next(fi).split()]

        # h[start] = int(w_st)
        # h[end] = int(w_ed)
        f[start], f[end] = 0, 0
        g[start], g[end] = 0, 0
        for line in fi:
            a, w_a, b, w_b, e = [str(x) for x in line.split()]
            h[a] = int(w_a)
            h[b] = int(w_b)
            f[a], f[b] = 0, 0
            g[a], g[b] = 0, 0
            k[(a, b)] = int(e)
            graph[a].append(b)
            if b == end:
                count += 1


def Branch_Bound(st, ed):
    with open(FILE_OUT, 'w') as fo:
        print("%s %60s" % ("\n", "Branch and Bound"), file=fo)
        print('-' * TABLE_WIDTH, file=fo)
        print("| %-10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-30s | %-40s |" % (
            'TT', 'TTK', 'k(u,v)', 'h(v)', 'g(v)', 'f(v)', 'DS L1', 'Danh sach L'), file=fo)
        print('-' * TABLE_WIDTH, file=fo)

        ct = 0
        cost = 0
        path = [(f[st], st)]
        queue = [path.copy()]

        while queue:
            path = queue.pop(0)
            front = path.pop(0)

            if len(path) > 0:  # not insert [] to queue
                queue.insert(0, path)

            if front[1] == ed:
                print('| %-10s | %-95s | %-40s |' % (
                    front[1], f'TTKT, tim duoc duong di tam thoi, do dai {f[front[1]]}', ' ' * 40), file=fo)
                cost = max(cost, f[front[1]])
                ct += 1
                if ct == count:
                    l = ', '.join([fm(x) for x in format_queue(queue)])
                    print('| %10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-30s | %-40s |' % (
                        ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, l1, l), end="\n", file=fo)
                    print('-' * TABLE_WIDTH, file=fo)
                    return
            else:
                print('| %-10s | %10s | %-10s | %-10s | %-10s | %-10s | %-30s | %-40s |' % (
                    front[1], ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 30, ' ' * 40), file=fo)

            next_path = []
            for e in graph[front[1]]:
                g[e] = g[front[1]] + k[(front[1], e)]
                f[e] = g[e] + h[e]
                next_path.append((f[e], e))
                print('| %10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-30s | %-40s |' % (
                ' ' * 10, e, k[front[1], e], h[e], g[e], f[e], 30 * ' ', 40 * ' '), end="\n", file=fo)

            if len(next_path) > 0:
                queue.insert(0, sorted(next_path.copy()))

            l1 = ', '.join([fm((f[x], x)) for x in sorted(graph[front[1]])])
            l = ', '.join([fm(x) for x in format_queue(queue)])
            print('| %10s | %-10s | %-10s | %-10s | %-10s | %-10s | %-30s | %-40s |' % (
                ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, ' ' * 10, l1, l), end="\n", file=fo)
            print('-' * TABLE_WIDTH, file=fo)

    print('Khong di duoc', file=fo)


if __name__ == '__main__':
    make_graph()
    Branch_Bound(start, end)
