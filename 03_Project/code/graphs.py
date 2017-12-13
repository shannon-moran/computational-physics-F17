# Import needed packages
import time
from tqdm import tqdm,tqdm_notebook
import itertools
import numpy as np
import random
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt


class Graph(object):

    def __init__(self,n,m,process_name):
        self.n = int(n)
        self.m = int(m)
        self.n_list = np.linspace(0,self.n-1,self.n).astype(int)
        self.edge_density = m/n
        self.phi = self.edge_density/n
        # tracks edges & orders them by when they were added
        self.edges = np.zeros((n,n),dtype=np.dtype('f4'))
        self.nodes = 0
        self.LJ = 0
        self.process = process_name

    def build(self):
        if self.process=='C-ODER': self.CODER()
        elif self.process=='ODER': self.ODER()
        elif self.process=='DER': self.DER()
        else: print('build with a valid process')

    def add_edge(self,p):
        if self.edges[p[0],p[1]]:
            if self.edges[p[1],p[0]]: pass
            else: self.nodes+=1; self.edges[p[1],p[0]] = self.nodes
        else: self.nodes+=1; self.edges[p[0],p[1]] = self.nodes

    def CODER(self):
        pbar = tqdm_notebook(total=(self.m-self.nodes),desc="Building C-ODER graph")
        while self.nodes<self.m:
            first_node, second_node, third_node = random.sample(list(self.n_list),3)
            proposed_edges = tuple(itertools.combinations(tuple(sorted((first_node,second_node,third_node))), 2))
            # for nodes with min difference, check if they/their reverse already exist; if no, add them
            difference = np.asarray([nodes[1]-nodes[0] for nodes in proposed_edges])
            idx = np.where(difference == difference.min())[0]
            n0 = self.nodes
            for i in idx:
                proposed_edge = proposed_edges[i]
                self.add_edge(proposed_edge)
            pbar.update(self.nodes-n0)
        pbar.close()

    def ODER(self):
        pbar = tqdm_notebook(total=(self.m-self.nodes),desc="Building ODER graph")
        while self.nodes<self.m:
            first_node, second_node = random.sample(list(self.n_list),2)
            proposed_edge = tuple(sorted((first_node,second_node)))
            n0 = self.nodes
            self.add_edge(proposed_edge)
            pbar.update(self.nodes-n0)
        pbar.close()

    def DER(self):
        pbar = tqdm_notebook(total=(self.m-self.nodes),desc="Building DER graph")
        while self.nodes<self.m:
            first_node, second_node = random.choice(list(self.n_list)),random.choice(list(self.n_list))
            proposed_edge = tuple((first_node,second_node))
            n0 = self.nodes
            self.add_edge(proposed_edge)
            pbar.update(self.nodes-n0)
        pbar.close()
