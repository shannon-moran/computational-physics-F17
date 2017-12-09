# test.py

from tools import *
import graphs as g
import pickle

PIK = "pickle.dat"

def figure56(process,edge_densities,n):
    largest_scc = []
    Sample = g.Graph(n,edge_densities[0]*n,process)
    for density in edge_densities:
        Sample.m = round(density*n)
        Sample.initialize()
        largest_scc.append(ranked_SCC(tarjan(Sample.edges))/n)
    return largest_scc

if __name__ == '__main__':
    n = int(1e5)
    # actual phi run in the experiment
    phi = np.linspace(1e-6,5e-5,8)
    # phi = np.linspace(1e-4,5e-3,8)
    edge_densities = phi*n
    print(edge_densities)
    replicates = 1

    # ODER_graph = g.Graph(n,phi[0]*n**2,'ODER')
    # print(ODER_graph.m)
    # for phii in phi:
    #     ODER_graph.m = round(int(phii*n**2))
    #     ODER_graph.initialize()

    for i in range(replicates):
        plt.plot(phi,figure56('ODER',edge_densities,n))
    plt.title('Explosive percolation of ODER process')
    plt.ylabel('Largest SCC')
    plt.xlabel('Edge density')
    plt.show()
