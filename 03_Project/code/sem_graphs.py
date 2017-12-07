# -*- coding: utf-8 -*-
#    Copyright (C) 2004-2017 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
"""
Generators for random graphs.
"""

from __future__ import division
import itertools
import math
import random

# ADDED BY SHANNON
import functools

import networkx as nx
from networkx.generators.classic import empty_graph, path_graph, complete_graph
from networkx.generators.degree_seq import degree_sequence_tree
from collections import defaultdict

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# __all__ = ['fast_gnp_random_graph',
#            'gnp_random_graph',
#            'dense_gnm_random_graph',
#            'gnm_random_graph',
#            'erdos_renyi_graph',
#            'binomial_graph',
#            'newman_watts_strogatz_graph',
#            'watts_strogatz_graph',
#            'connected_watts_strogatz_graph',
#            'random_regular_graph',
#            'barabasi_albert_graph',
#            'extended_barabasi_albert_graph',
#            'powerlaw_cluster_graph',
#            'random_lobster',
#            'random_shell_graph',
#            'random_powerlaw_tree',
#            'random_powerlaw_tree_sequence',
#            'random_kernel_graph']


#-------------------------------------------------------------------------
#  Some Famous Random Graphs
#-------------------------------------------------------------------------


def fast_gnp_random_graph(n, p, seed=None, directed=False):
    """Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph or
    a binomial graph.
    Parameters
    ----------
    n : int
        The number of nodes.
    p : float
        Probability for edge creation.
    seed : int, optional
        Seed for random number generator (default=None).
    directed : bool, optional (default=False)
        If True, this function returns a directed graph.
    Notes
    -----
    The $G_{n,p}$ graph algorithm chooses each of the $[n (n - 1)] / 2$
    (undirected) or $n (n - 1)$ (directed) possible edges with probability $p$.
    This algorithm [1]_ runs in $O(n + m)$ time, where `m` is the expected number of
    edges, which equals $p n (n - 1) / 2$. This should be faster than
    :func:`gnp_random_graph` when $p$ is small and the expected number of edges
    is small (that is, the graph is sparse).
    See Also
    --------
    gnp_random_graph
    References
    ----------
    .. [1] Vladimir Batagelj and Ulrik Brandes,
       "Efficient generation of large random networks",
       Phys. Rev. E, 71, 036113, 2005.
    """
    G = empty_graph(n)

    if seed is not None:
        random.seed(seed)

    if p <= 0 or p >= 1:
        return nx.gnp_random_graph(n, p, directed=directed)

    w = -1
    lp = math.log(1.0 - p)

    if directed:
        G = nx.DiGraph(G)
        # Nodes in graph are from 0,n-1 (start with v as the first node index).
        v = 0
        while v < n:
            lr = math.log(1.0 - random.random())
            w = w + 1 + int(lr / lp)
            if v == w:  # avoid self loops
                w = w + 1
            while v < n <= w:
                w = w - n
                v = v + 1
                if v == w:  # avoid self loops
                    w = w + 1
            if v < n:
                G.add_edge(v, w)
    else:
        # Nodes in graph are from 0,n-1 (start with v as the second node index).
        v = 1
        while v < n:
            lr = math.log(1.0 - random.random())
            w = w + 1 + int(lr / lp)
            while w >= v and v < n:
                w = w - v
                v = v + 1
            if v < n:
                G.add_edge(v, w)
    return G

def add_edge(edges, G, p):
    for e in edges:
        if random.random() < p:
            G.add_edge(e)

def gnp_random_graph(n, p, seed=None, directed=False):
    """Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph
    or a binomial graph.
    The $G_{n,p}$ model chooses each of the possible edges with probability $p$.
    The functions :func:`binomial_graph` and :func:`erdos_renyi_graph` are
    aliases of this function.
    Parameters
    ----------
    n : int
        The number of nodes.
    p : float
        Probability for edge creation.
    seed : int, optional
        Seed for random number generator (default=None).
    directed : bool, optional (default=False)
        If True, this function returns a directed graph.
    See Also
    --------
    fast_gnp_random_graph
    Notes
    -----
    This algorithm [2]_ runs in $O(n^2)$ time.  For sparse graphs (that is, for
    small values of $p$), :func:`fast_gnp_random_graph` is a faster algorithm.
    References
    ----------
    .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    """
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return complete_graph(n, create_using=G)

    if seed is not None:
        random.seed(seed)

    if G.is_directed():
        edges = itertools.permutations(range(n), 2)
    else:
        edges = itertools.combinations(range(n), 2)

    for e in edges:
        if random.random() < p:
            G.add_edge(*e)
    return G
