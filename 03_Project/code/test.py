# test.py

from tools import *
import graphs as g
# import pickle

# PIK = "pickle.dat"

def figure56(process,edge_densities,n):
    largest_scc = []
    Sample = g.Graph(n,edge_densities[0]*n,process)
    for density in edge_densities:
        Sample.m = round(density*n)
        Sample.build()
        largest_scc.append(ranked_SCC(tarjan(Sample.edges))/n)
    return largest_scc

'''
Wow, okay, my lab desktop is way faster than warhol/vizlab for doing analysis
Pepitone is running at about 270it/s, warhol was running at about 170it/s, and a flux login node was running at about 140it/s (71s to add 10k edges)
flux - no
vizlab - no
Pepitone - good option for running things that work a little bit longer
macbook - can run slightly smaller stuff
'''

if __name__ == '__main__':
    n = int(1e4)
    # actual phi run in the experiment
    # phi = np.linspace(1e-6,5e-5,8)
    phi = np.linspace(1e-4,5e-3,5)
    edge_densities = phi*n
    print(edge_densities)
    replicates = 1

    for i in range(replicates):
        plt.plot(edge_densities,figure56('ODER',edge_densities,n))
    plt.title('Explosive percolation of ODER process')
    plt.ylabel('Largest SCC')
    plt.xlabel('Edge density')
    plt.show()
