import random
import itertools

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm,tqdm_notebook

class Graph(object):

    def __init__(self,n,m,process_name,verbal=False):
        ''' Initializes a base graph with n nodes, no edges yet

        Parameters
        ------
        n : number of nodes (int)
        m : number of edges (int)
            Edges are not actually built until build() is called
        process_name : type of graph to be built (str)
            Valid options: 'C-ODER', 'ODER', 'DER'
        '''

        self.n = int(n)
        self.m = int(m)
        self.v = verbal  # 'verbal' flag used to turn progress bars on/off
        self.process = process_name

        # Graph characterization
        self.edge_density = m/n
        self.n_list = np.linspace(0,self.n-1,self.n).astype(int) # list of all nodes

        # Adjacency matrix `edges` is an (n,n) numpy array used to store all edges
        self.edges = np.zeros((n,n),dtype=np.dtype('f4'))

        # Not all proposed edges will be accepted
        # `edge_count` is the equivalent of np.sum(self.edges!=0)
        self.edge_count = 0

    def build(self):
        ''' Makes sure user requests a valid process, then calls appropriate graph building routine
        '''
        if self.process=='C-ODER': self.CODER()
        elif self.process=='ODER': self.ODER()
        elif self.process=='DER': self.DER()
        else: print('build with a valid process')

    def add_edge(self,p):
        ''' Checks if edge OR reverse edge exists before adding proposed edge

        Parameters
        -----
        p : proposed edge (tuple)
            Random edge proposed during process-specific build routines (below)
        '''

        if self.edges[p[0],p[1]]:
            if self.edges[p[1],p[0]]: pass
            else: self.edge_count+=1; self.edges[p[1],p[0]] = self.edge_count
        else: self.edge_count+=1; self.edges[p[0],p[1]] = self.edge_count

    def DER(self):
        ''' Directed Erdos-Renyi Graph routine (DER)
        '''
        if self.v: pbar = tqdm_notebook(total=(self.m-self.edge_count),desc="Building DER graph")

        # Add edges to current graph until number of edges on graph equals target, m
        while self.edge_count<self.m:
            # Pick two random edges to propose; order does not matter
            first_node, second_node = random.choice(list(self.n_list)),random.choice(list(self.n_list))
            proposed_edge = tuple((first_node,second_node))

            # Run add_edge routine to check if edge/reverse edge exists; if not, add
            n0 = self.edge_count
            self.add_edge(proposed_edge)
            if self.v: pbar.update(self.edge_count-n0)

        if self.v: pbar.close()

    def ODER(self):
        ''' Ordered, Directed Erdos-Renyi Graph routine (ODER)
        '''
        if self.v: pbar = tqdm_notebook(total=(self.m-self.edge_count),desc="Building ODER graph")

        # Add edges to current graph until number of edges on graph equals target, m
        while self.edge_count<self.m:
            # Pick two random edges to propose; sort so rank of head>tail
            first_node, second_node = random.sample(list(self.n_list),2)
            proposed_edge = tuple(sorted((first_node,second_node)))

            # Run add_edge routine to check if edge/reverse edge exists; if not, add
            n0 = self.edge_count
            self.add_edge(proposed_edge)
            if self.v: pbar.update(self.edge_count-n0)

        if self.v: pbar.close()

    def CODER(self):
        ''' Competitive, Ordered, Directed Erdos-Renyi Graph routine (C-ODER)
        '''
        if self.v: pbar = tqdm_notebook(total=(self.m-self.edge_count),desc="Building C-ODER graph")

        # Add edges to current graph until number of edges on graph equals target, ms
        while self.edge_count<self.m:
            # Pick three random nodes and propose edges between all of them
            first_node, second_node, third_node = random.sample(list(self.n_list),3)
            proposed_edges = tuple(itertools.combinations(tuple(sorted((first_node,second_node,third_node))), 2))

            # Only propose the edge with the smallest difference between the node ranks
            # If multiple edges have the same difference between ranks, propose both edges
            difference = np.asarray([nodes[1]-nodes[0] for nodes in proposed_edges])
            idx = np.where(difference == difference.min())[0]
            n0 = self.edge_count
            for i in idx:
                proposed_edge = proposed_edges[i]
                self.add_edge(proposed_edge)
            if self.v: pbar.update(self.edge_count-n0)

        if self.v: pbar.close()
