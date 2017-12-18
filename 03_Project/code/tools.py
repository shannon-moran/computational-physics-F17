# Import needed packages
import time
import itertools
import numpy as np
import random
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

# =========
# Helper functions
# =========

# =========
# Component clustering algorithm
# =========

def tarjan(edges):
        index_counter = [0]
        index = {}
        lowlink = {}
        stack = []

        result = []

        # v is node-- wait, but shouldn't it actually be u...?
        def calc_component(node):
            # v.index, v.lowlink
            index[node] = index_counter[0]
            lowlink[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)

            # find the children
            try:
                children = np.where(edges[node]!=0)[0] # i think this actually needs to have 1 added to it...?
            except:
                children = []
            for child in children:
                # if the child hasn't been visited, run this on it
                if child not in lowlink:
                    calc_component(child)
                    lowlink[node] = min(lowlink[node],lowlink[child])
                # if the child is in the stack, that means they're also in the SCC
                elif child in stack:
                    lowlink[node] = min(lowlink[node],index[child])

            if lowlink[node]==index[node]:
                connected_component = []
                while True:
                    successor = stack.pop()
                    connected_component.append(successor)
                    if successor == node: break
                component = tuple(connected_component)
                # storing the result
                result.append(component)

        for node in range(edges.shape[0]):
            if node not in lowlink:
                calc_component(node)

        return result

# =========
# Algorithms from the paper
# =========

'''
input: connected components (list of tuples)
output: size of SCC of given rank size (scalar)
'''
def ranked_SCC(connected_components,rank=1):
    C = []
    for members in connected_components:
        C.append(len(members))
    if rank>len(C): return 0
    return sorted(C)[-rank]

'''
Ah, switching from using tuple edges and order means i have to switch how I do this
'''
def binary_search(graph,start,end,LJ):
    midpoint = int(round((start+end)/2))
    head = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=start)))
    mid = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=midpoint)))
    tail = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=end)))
    # print(start, midpoint, end)
    # print(head,mid,tail)
    if abs(end-start)==1:
        if (tail-head)>LJ: LJ = (tail-head)
        return LJ
    elif (mid-head)>(tail-mid):
        if (mid-head)>(graph.n/100):
            LJ = (mid-head)
            return binary_search(graph,start,midpoint,LJ)
    elif (tail-mid)>(graph.n/100):
        LJ = (tail-mid)
        return binary_search(graph,midpoint,end,LJ)
    return LJ

def get_largest_jump(graph):
    start = 1
    midpoint = int(round(graph.m/2))
    end = graph.m-1
    head = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=start)))
    mid = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=midpoint)))
    tail = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=end)))
    # print(start,midpoint,end)
    # print(head,mid,tail)
    LJ = 0
    if (tail-head)<(graph.n/100): jump = (tail-head)
    else: jump = binary_search(graph,start,midpoint,LJ)
    # print('jump: %s'%jump)
    return jump
#
# def nothing():
#     pass
