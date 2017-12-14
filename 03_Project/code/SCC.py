# -*- coding: utf-8 -*-
"""Strongly connected components.
"""
#    Copyright (C) 2004-2013 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
import networkx as nx
from networkx.utils.decorators import not_implemented_for
__authors__ = "\n".join(['Eben Kenah',
                         'Aric Hagberg (hagberg@lanl.gov)'
                         'Christopher Ellison',
                         'Ben Edwards (bedwards@cs.unm.edu)'])

__all__ = ['number_strongly_connected_components',
           'strongly_connected_components',
           'strongly_connected_component_subgraphs',
           'is_strongly_connected',
           'strongly_connected_components_recursive',
           'kosaraju_strongly_connected_components',
           'condensation']

def strongly_connected_components(G):
    """Generate nodes in strongly connected components of graph.

    Parameters
    ----------
    G : NetworkX Graph
       An directed graph.

    Returns
    -------
    comp : generator of lists
       A list of nodes for each strongly connected component of G.

    Raises
    ------
    NetworkXNotImplemented: If G is undirected.

    See Also
    --------
    connected_components, weakly_connected_components

    Notes
    -----
    Uses Tarjan's algorithm with Nuutila's modifications.
    Nonrecursive version of algorithm.

    References
    ----------
    .. [1] Depth-first search and linear graph algorithms, R. Tarjan
       SIAM Journal of Computing 1(2):146-160, (1972).

    .. [2] On finding the strongly connected components in a directed graph.
       E. Nuutila and E. Soisalon-Soinen
       Information Processing Letters 49(1): 9-14, (1994)..
    """
    preorder={}
    lowlink={}
    scc_found={}
    scc_queue = []
    i=0     # Preorder counter
    for source in G:
        if source not in scc_found:
            queue=[source]
            while queue:
                v=queue[-1]
                if v not in preorder:
                    i=i+1
                    preorder[v]=i
                done=1
                v_nbrs=G[v]
                for w in v_nbrs:
                    if w not in preorder:
                        queue.append(w)
                        done=0
                        break
                if done==1:
                    lowlink[v]=preorder[v]
                    for w in v_nbrs:
                        if w not in scc_found:
                            if preorder[w]>preorder[v]:
                                lowlink[v]=min([lowlink[v],lowlink[w]])
                            else:
                                lowlink[v]=min([lowlink[v],preorder[w]])
                    queue.pop()
                    if lowlink[v]==preorder[v]:
                        scc_found[v]=True
                        scc=[v]
                        while scc_queue and preorder[scc_queue[-1]]>preorder[v]:
                            k=scc_queue.pop()
                            scc_found[k]=True
                            scc.append(k)
                        yield scc
                    else:
                        scc_queue.append(v)
