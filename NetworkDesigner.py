import math
import time
from itertools import combinations
import matplotlib.pyplot as plt
from tqdm import tqdm
from Edge import Edge

path = './tester/5_city.txt'
global NUM_NODE, BUDGET


def connected(edges):   # @Alex
    def dfs(n, g, visited):
        """
        DEPTH-FIRST SEARCH TRAVERSAL
            :param n:       current node being visited;
            :param g:       adjacency list representation of the graph;
            :param visited: boolean list to record visited nodes.
        """
        visited[n] = 1
        for neighbour in g[n]:
            if not visited[neighbour]:
                dfs(neighbour, g, visited)

    graph = [[] for _ in range(NUM_NODE)]
    is_visited = [0] * NUM_NODE
    for e in edges:
        graph[e.get_city_a()].append(e.get_city_b())
        graph[e.get_city_b()].append(e.get_city_a())
    dfs(0, graph, is_visited)
    return all(is_visited)  # nx.is_connected(G)


# RETURNS RELIABILITY OF THE GRAPH RECURSIVELY
def r_g(edges, reliable):   # @Zhanyue
    e_sorted = sorted(edges, key=lambda x: x.get_city_a(), reverse=True)
    if not connected(e_sorted + reliable):
        return 0
    elif len(e_sorted + reliable) == NUM_NODE - 1:
        return math.prod(e.get_reliability() for e in edges)
    else:
        if len(e_sorted) > 0:
            r = 0
            e = e_sorted[0]
            cloned = e_sorted.copy()
            cloned.remove(e)
            r += (1 - e.get_reliability()) * r_g(cloned, reliable)
            reliable.append(e)
            r += e.get_reliability() * r_g(cloned, reliable)
            return r
        else:
            return 1


def draw(edges, c, r, title='ADVANCED'):    # @Fengqi
    angle = 2 * math.pi / NUM_NODE
    points, labels = [], []
    for i in range(NUM_NODE):
        x, y = math.cos(i * angle), math.sin(i * angle)
        points.append((x, y))
        labels.append(i + 1)
    x, y = zip(*points)  # separate x & y
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i in range(len(labels)):
        ax.text(x[i], y[i], labels[i], fontsize=12)
    for e in edges:
        idx_a, idx_b = e.get_city_a(), e.get_city_b()
        ax.plot([x[idx_a], x[idx_b]], [y[idx_a], y[idx_b]])
    plt.text(-1, -1, f"Cost {c}, maxR {r:.6f}")
    ax.axis('off')
    ax.set_title(title)
    plt.show()


def optimizer(edges):   # @Zhanyue & Alex
    # KRUSKAL'S: MINIMUM SPANNING TREE WITH DISJOINT-SET DATA STRUCTURE
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    mst = []    # nx.minimum_spanning_tree(G)
    parent = {i: i for i in range(NUM_NODE)}  # init parent dictionary
    for e in edges:
        if len(mst) == NUM_NODE - 1:
            break
        root_a, root_b = find(e.get_city_a()), find(e.get_city_b())
        if root_a != root_b:
            parent[root_a] = root_b
            mst.append(e)
    mst_pro = mst.copy()
    e_rest = [e for e in edges if e not in mst]
    cost = sum(e.get_cost() for e in mst)
    r_max = math.prod(e.get_reliability() for e in mst)
    while BUDGET - cost >= min([e.cost for e in e_rest]):
        r_rest, c_rest, ratio, available = [[0] * len(e_rest) for _ in range(4)]
        for i, e in enumerate(e_rest):
            replica = mst_pro.copy() + [e]
            c_rest[i] = sum(e.get_cost() for e in replica)
            if c_rest[i] > BUDGET:
                ratio[i] = -1
                continue
            r_rest[i] = r_g(replica, [])
            ratio[i] = r_rest[i] / c_rest[i]
            available[i] = (BUDGET - sum(e.get_cost() for e in replica) >=
                            min([e.cost for e in e_rest[:i] + e_rest[i + 1:]]))
        r_max = max(r_rest)
        i = ratio.index(max(ratio))
        idx = i if i == r_rest.index(r_max) or available[i] == 1 else r_rest.index(r_max)
        mst_pro.append(e_rest[idx])
        cost = sum(e.get_cost() for e in mst_pro)
        e_rest.pop(idx)
    return mst_pro, cost, r_max, sum(e.get_cost() for e in mst) <= BUDGET


def main():  # @Alex
    # 1. REQUIREMENT VALIDATION
    global NUM_NODE, BUDGET
    rt1, rt2 = 0.0, 0.0
    while True:
        try:
            BUDGET = int(input("Please specify cost limit: "))
            assert BUDGET > 0
            break
        except (ValueError, AssertionError) as err:
            print("INVALID INPUT: ", err)

    # 2. PARSE TESTER TEXT
    edges, matrix_r, matrix_c = [], [], []
    with open(path, 'r') as file:
        lines = file.readlines()
        try:
            NUM_NODE = int(lines[3].strip())
        except (ValueError, IndexError):
            raise ValueError("VOID NUMBER OF NODES IN PROVIDED FILE.")
        for line in lines[8: 2 * NUM_NODE + 5]:
            if not line.startswith('#') and line.strip():
                matrix_r.extend(map(float, line.split()))
        for line in lines[- NUM_NODE - 2:]:
            if not line.startswith('#') and line.strip():
                matrix_c.extend(map(int, line.split()))
    for i in range(NUM_NODE):
        for j in range(i + 1, NUM_NODE):
            e = Edge(i, j)
            e.set_reliability(matrix_r.pop(0))
            e.set_cost(matrix_c.pop(0))
            edges.append(e)
    n = len(edges)  # number of distinct city pairs <=> NUM_NODE * (NUM_NODE - 1) // 2
    e_r = sorted(edges, key=lambda x: (x.reliability, -x.cost), reverse=True)
    e_c = sorted(edges, key=lambda x: (x.cost, -x.reliability))

    # 3. GUIDED SEARCH @Zhanyue & Alex
    t1 = time.time()
    *mst_r, r_feasible = optimizer(e_r)  # reliability-greedy part
    *mst_c, c_feasible = optimizer(e_c)  # cost-greedy part
    if r_feasible or c_feasible:
        rt1 = (time.time() - t1) * 1000
        print(f"Runtime for advanced algo: {rt1:.4f} ms\n")
        draw(*mst_r if mst_r[2] > mst_c[2] else mst_c)  # reliability-based choice

    # 4. EXHAUSTIVE SEARCH @Fengqi
    t2 = time.time()
    optima = None
    r_optima, c_optima = 0, 0
    j = 1
    while j < n and (c_optima := c_optima + e_c[j - 1].cost) <= BUDGET:
        j += 1
    pbar = tqdm(total=sum(math.comb(n, k) for k in range(NUM_NODE - 1, j)))
    for i in range(NUM_NODE - 1, j):
        for comb in combinations(e_c, i):
            if (c := sum(e.cost for e in comb)) <= BUDGET and connected(comb):
                if (r := r_g(comb, [])) > r_optima:
                    r_optima, c_optima = r, c
                    optima = comb
            pbar.update(1)
    pbar.close()
    if optima:  # expecting is not None
        rt2 = (time.time() - t2) * 1000
        print(f"Runtime for simple algo: {rt2:.4f} ms")
        print(f"Relatively {((rt2 - rt1) / rt1 * 100):.0f}% slower" if rt1 != 0
              else "SIMPLE NETWORK, MACRO PERFORMANCE DISCREPANCY NEGLIGIBLE")
        draw(optima, c_optima, r_optima, 'SIMPLE')
    else:
        print("INFEASIBLE CASE. PROGRAM TERMINATED.")


if __name__ == "__main__":
    main()
