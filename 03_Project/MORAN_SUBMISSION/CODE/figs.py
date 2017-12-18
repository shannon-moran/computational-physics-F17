import random

import numpy as np
import matplotlib.pyplot as plt

from clustering import *
from critical_exponents import *
import graphs as g

def figure56(process,n,edge_densities,replicates):
    plt.figure(figsize=(5,4))
    for replicate in range(replicates):
        largest_scc = []
        Sample = g.Graph(n,round(edge_densities[0]*n),process)
        for density in edge_densities:
            Sample.m = round(density*n)
            Sample.build()
            largest_scc.append(ranked_SCC(tarjan(Sample.edges>0))/n)
        plt.plot(edge_densities,largest_scc)
    plt.title('Explosive percolation of %s process, n=%d' %(process,n))
    plt.ylabel('Largest SCC')
    plt.xlabel('Edge density')
    plt.show()

def figure7(process,n_sizes,edge_density,replicates):
    jumps = []
    for replicate in range(replicates):
        max_jump = []
        # Sample = g.Graph(n_sizes[0],edge_density*n_sizes[0],process)
        for n in n_sizes:
            Sample = g.Graph(n,edge_density*n,process)
            Sample.build()
            max_jump.append(get_largest_jump(Sample)/n)
        jumps.append(max_jump)
    Jumps_array = np.asarray(jumps).reshape((replicates,len(jumps[0])))
    Avg_jump= np.mean(Jumps_array, axis=0)
    Std_jump= np.std(Jumps_array, axis=0)
    plt.errorbar(n_sizes,Avg_jump,yerr=Std_jump, fmt='o')
    if process=="C-ODER": plt.axis([0,max(n_sizes)*1.1,0.25,0.45])
    elif process=="ODER": plt.axis([0,max(n_sizes)*1.1,-0.05,0.20])
    plt.title('Max jump size, %s' %process)
    plt.ylabel('Max jump')
    plt.xlabel('System size')
    plt.show()

def figure8(process,n,edge_densities):
    first_scc,second_scc,third_scc = [],[],[]
    Sample = g.Graph(n,round(edge_densities[0]*n),process)
    for density in edge_densities:
        Sample.m = round(density*n)
        Sample.build()
        first_scc.append(ranked_SCC(tarjan(Sample.edges),rank=1)/n)
        second_scc.append(ranked_SCC(tarjan(Sample.edges),rank=2)/n)
        third_scc.append(ranked_SCC(tarjan(Sample.edges),rank=3)/n)
    plt.scatter(edge_densities,first_scc,label="Largest SCC")
    plt.scatter(edge_densities,second_scc,label="Second largest SCC")
    plt.scatter(edge_densities,third_scc,label="Third largest SCC")
    plt.title('%s process: SCC combination near critical edge density, n=%d' %(process,n))
    plt.ylabel('Component size')
    plt.xlabel('Edge density')
    plt.legend()
    plt.show()
