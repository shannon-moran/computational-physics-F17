from tools import *
import graphs as g
import figs as f

edge_densities = np.linspace(10,50,5)
# edge_densities = [50]
n = int(1e2)
reps = 1
f.figure56('ODER',n,edge_densities,reps)
