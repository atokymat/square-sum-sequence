import math

def read_dict():
    graph = {}
    with open('dict.txt') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip().split(':')
            if line[1] == '':
                graph[int(line[0])] = []
            else:
                graph[int(line[0])] = [int(x) for x in (line[1].split(','))]
    return graph

def write_dict(graph):
    with open('dict.txt', 'w') as f:
        for (key,val) in graph.items():
            f.write(str(key) + ":" + str(val).replace(' ', '')[1:-1]+"\n")

def append_dict(graph, n):
    graph[n] = []
    for i in range(len(squares)):
        s = squares[i] - n
        if 0<s<n:
            graph[s].append(n)
            graph[n].append(s)
    return graph

def fill_from_empty(maximum, write=True):
    graph = {1:[]}
    for i in range(1, maximum+1):
        graph = append_dict(graph, i)
    if write:
        write_dict(graph)
    return graph

def fill_range(graph, start, end, write=True):
    for i in range(start+1, end+1):
        graph = append_dict(graph, i)
    if write:
        write_dict(graph)
    return graph

# def h_path_exists_btw(graph, start, end, n_nodes, path=[]):
#     path = path + [start]
#     if len(path) == n_nodes:
#         return True
#     if start == end:
#         return n_nodes == 1
#     for node in graph[start]:
#         if node not in path:
#             newpath = h_path_exists_btw(graph, node, end, n_nodes, path)
#             if newpath:
#                 return True
#     return False

def heuristic_sort(graph, n_nodes=-1):
    keys = list(graph.keys())
    if n_nodes == -1: n_nodes = len(keys)

    ne = [ [k, 0, []] for k in keys ]

    for i in range(n_nodes):
        neighbours = graph[ne[i][0]]
        for j in range(n_nodes):
            if keys[j] in neighbours:
                ne[i][2].append(j)
        ne[i][1] = len(neighbours)

    for i in range(n_nodes):
        graph[ne[i][0]] = [ ne[n][0] for n in sorted(ne[i][2], key = lambda x: ne[1]) ]

    return [ n[0] for n in sorted(ne, key = lambda x: x[1]) ]

def h_path_exists(graph, n_nodes=-1):
    if n_nodes == -1: n_nodes = len(graph.keys())
    nodes = heuristic_sort(graph, n_nodes)
    for startnode in nodes:
        stack = [ [startnode, [startnode], 1] ]
        while len(stack) > 0:
            next = stack[-1]
            node = next[0]
            del stack[-1]
            for n in graph[node]:
                if n not in next[1]:
                    if next[2]+1 == n_nodes:
                        return True
                    stack.append( [n, next[1]+[n], next[2]+1] )
    return False


def known_network(max_int, value):
    with open('knownnetworks.txt', 'a') as f:
        f.write(str(max_int) + '\t' + str(value) + '\n')

def reset_all():
    a = input('Confirm deletion? (y/n): ')
    if a == ('y'):
        with open('knownnetworks.txt', 'w') as f:
            f.write('')
        with open('dict.txt', 'w') as f:
            f.write('')
        quit()

def last_known_node():
    x = 0
    try:
        with open('knownnetworks.txt', 'r') as f:
            lines = f.readlines()
            x = int(lines[-1].split('\t')[0])
    except:
        pass
    return x

# This value can be changed
n = 10000 #planned maximum



squares = [x*x for x in range(1,math.floor(math.sqrt(2*n-1))+1)]
last_known = last_known_node()
g = read_dict()

try:
    i = last_known+1
    g[i]
    # If we know the edges for one more vertex, then "catch up" the knowledge of known networks
    is_connected = h_path_exists(g, i)
    known_network(i, is_connected)
    print("Integers to " + str(i) + " is " + str(is_connected))
    last_known = i
except KeyError:
    # If the knowledge is "up-to-date" then no need for a calculation
    pass


for i in range(last_known+1, n):
    # Fills in the next node and determines whether a square-sum list can exist for 1, ..., i
    g = fill_range(g, i-1, i)
    is_connected = h_path_exists(g, i)
    known_network(i, is_connected)
    print("Integers to " + str(i) + " is " + str(is_connected))
