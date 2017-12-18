# Modeling explosive percolation on directed networks
Shannon Moran
PHYS 514, Final Project Fall 2017

## Motivation
- Wanted to take what we'd learned and apply it to a recent problem
- I do molecular dynamics as my day job, so I wanted to do something that wasn't that
- The reason I like grad classes is that they give me a strong foundation to go out and understand other parts of the field

Paper:
- In July, a group out of UC-Davis published a paper looking to replicate the observed trends of tweets in response to the discovery of the Higgs boson
- This data set is publicly available as part of the Stanford Large Network Dataset Collection, so folsk have looked to study it
- These authors saw the growth of the tweet network and recognized it as explosive Percolation

Percolation
- Explosive percolation  is said to occur in an evolving network when a macroscopic connected component emerges in a number of steps that is much smaller than the system size, and there's been a number of papers [e.g. the two that Ziff sent me] that have explored this phenomena in random networks.

Why this paper:
I particularly liked this paper because it took topics that we had covered in class and extended them on a number of directions.

|  | Studied in class | Used in the paper |
| :------------- | :------------- | :------------- |
| **Percolation process** | *Site* percolation on a *lattice* | *Edge* percolation on a network of *nodes* |
| **Cluster definition** | Clusters of nearest-neighbor occupied sites | Strongly connected components |
| **Clustering algorithm**  | Hoshen-Kopelman | Tarjan's Algorithm (CITE), a depth-first search  |
| **Critical exponents**   | $\alpha$, $\beta$, $\nu$, $\eta$, $\gamma$  | $\beta$ (but a different $\beta$)  |

I will walk through each of the dimensions above, and show that I am able to replicate the findings from the paper.

## Methods

### Percolation process

Associated codes: `Graph` class, Section 1
 - process of putting together a graph
 - the three different types of graphs
 - what we find as a result

### Cluster definition and algorithms

Associated codes: `tarjan`
- what a strongly connected component is
- how the tarjan algorithm works

### Critical exponents

Associate codes: `binary_search`, `largest_scc`, `get_largest_jump`
-

### Results and discussion

See notes for metrics.
- $\phi = \frac{50}{10^6} = 5E-5 = $ fraction of a system that an average node reaches
- $m_0=$ average number of edges per node

We are better off studying a range of $\phi=\frac{m_0}{n}$, as this is more analogous to $p_c$ in percolation lattices.

As before, $n$ is the total number of nodes and $m$ is the total number of edges.

So our range of behaviors is:
- Lower bound: $m_0=1$, $n=2E4$, $m=2E4$
- Upper bound (paper): $m_0=50$, $n=1E6$, $m=50E6$
- General case: $m_0$, $n=\frac{m_0}{\phi}$, $m=m_0{\cdot}n$

In all cases, `edge_density` as defined in the paper is $\frac{m}{n}$== so just $m_0$.

In the paper, when they change the `edge_density`, what they are actually changing is the fraction of the system that any given node is connected to.

### Open question about the scaling

Associate code: `fig56`, `fig8`, `fig7`
