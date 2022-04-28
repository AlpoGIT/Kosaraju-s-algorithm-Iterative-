import numpy as np
from collections import defaultdict
import csv

'''
Compute strongly connected components of a directed graph
via Kosaraju's algorithm.
It's based on the stanford's edX course on algorithm.
The algorithm is as follows:
    1-  First run DFS on the transpose graph (all edges are reversed)
        The goal is to obtain a topological ordering such that the initial node
        has the biggest value. This is the only fact that is need to obtain a key lemma
        needed for the proof of correctness.
    2-  Run DFS on the original graph in decreasing topological order.
        Each DFS will output a SCC of the original graph.
'''

def first_pass_dfs(g,s,visited : list,f,t):
    '''
    input:  graph g as an adjacency list
            starting node s
            visited is the list of already explored nodes
            relabelling function f (the key purpose is to assign the biggest value to the node s)
            index t for track the relabelling

    output: explored list by dfs
            f
            t

    Comments: iterative DFS (since the recursive DFS can't manage big graphs)
    '''

    stack = []
    stack.append(s)
    visited[s] = True
    newly_visited = [] # this keeps track of the exploring order of DFS

    while stack:
        u = stack.pop(-1)
        newly_visited.append(u)

        for v in g[u]:
            if not visited[v] :
                visited[v] = True
                stack.append(v)

    # The only thing that matters is that the initial node has the biggest ordering
    # this is the only fact that is needed in the proof of key lemma.
    # So, take the explored list, and pop from last, so that f[s] > f[u] for all explored u != s.
    while newly_visited:
        u = newly_visited.pop(-1)
        t += 1
        f[u] = t

    return visited, f, t


def second_pass_dfs(g,s,visited : list):
    '''
    Input:  graph g
            starting node s
            list of explored nodes
            relabelling function f
            index t
    Output: visited
            explored nodes by DFS
    '''

    stack = []
    stack.append(s)
    visited[s] = True
    newly_explored_list = [s]

    while stack:
        u = stack.pop(-1)

        for v in g[u]:
            if not visited[v] :
                visited[v] = True
                stack.append(v)
                newly_explored_list.append(v)
                   
    return visited, newly_explored_list


def main_loop():
    '''
    Input: None
    Output: list of SCCs

    Comments:
    Let's say that you have C1 -> C2.
    In G_rev, you have C1 <- C2.
    When First_pass_DFS finishes, we have an ordering f with the following property:
    t_i := max_{u in C_i}f[u] < t_j := max_{u in C_j}f[u], for C_i -> C_j in G (when DFS is run on G_rev).
    In the proof, the key important thing is that the initial node 
    has the largest finishing time for a given DFS run.
    Here, t1 < t2.
    Now, run DFS on G from the biggest label t_i.
    Here, it starts from t2, so that DFS will output C2.
    then, it'll pop up C1.
    '''
    # Complete the 3 lines below
    location = '<ROOT>'
    name = '<FiLE NAME>.txt'
    n = <NUMBER OF NODES> # number of nodes

    # generate reversed graph
    print('Generate reversed graph')
    graph_rev = {}
    for i in range(n):
	    graph_rev[i] = []

    file = open(location+name,encoding='utf-8')
    csv_f = csv.reader(file,delimiter= ' ')
    for row in csv_f:
        graph_rev[int(row[1])-1].append(int(row[0])-1)

    # First pass
    print('Start first pass')

    explored = [False for _ in range(n)]
    f = defaultdict()
    t = -1

    # The order here is not important (see proof)
    # Run DFS on reversed graph
    for i in range(n): #np.random.choice(range(n),size=n,replace=False): 
        if not explored[i]:
            explored,f,t = first_pass_dfs(graph_rev,i,explored,f,t)

        # track some progress...
        if i%100000==0:
            print(f'Length of explored:\t{sum(explored)}')


    # generate relabeled transposed graph
    print('Generate relabeled original graph')
    graph = {}
    for i in range(n):
	    graph[i] = []

    file = open(location+name,encoding='utf-8')
    csv_f = csv.reader(file,delimiter= ' ')
    for row in csv_f:
        #shift all by -1
        graph[f[int(row[0])-1]].append(f[int(row[1])-1])

    # 2nd pass
    print('Start 2nd pass')
    SCC_counts = []
    SCCs = []
    explored = [False for _ in range(n)]

    # from biggest label (i.e. finishing times)
    for i in reversed(range(n)):
        if not explored[i]:
            explored, single_SCC = second_pass_dfs(graph,i,explored)

            SCC_counts.append(len(single_SCC))
            SCCs.append(single_SCC)

        if i%100000==0:
            print(f'Length of explored:\t{sum(explored)}')

    #Print the 5 biggest SCCs
    print(f'Your answer:\t{sorted(SCC_counts,reverse=True)[:5]}')
    #print(SCCS)

    return None

main_loop()
