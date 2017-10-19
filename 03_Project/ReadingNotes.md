# Reading notes on explosive directed percolation

From the overview:
> ... here we introduce two percolation models on a set of rank-ordered nodes where edges are added monotonically with respect to the rank ordering...

They claim this is analogous to networks such as Twitter followings/responses to the Higgs-Boson discovery.

## Model 1: Ordered, Directed Erdos-Renyi (ODER)
- Generalization of the directer ER model to ordered graph
- Form two large components, which explosively merge (discontinuous jump in the size of the largest strongly connected component)

## Model 2: Competitive ODER
- Adds competition: preference for connecting nodes of similar rank
- See similar discontinuous jump in cluster size, but "more explosive"
- Get an effective phase separation of the two large components: one containing the lower-ranked users, one containing the higher-ranked users
- TAKEAWAY: Some bias towards grouping similar-ranked nodes leads to formation of two distinct groups of nodes (classes) with little flow of information between the classes


## What I will actually do for this project
1. Implement ODER and C-ODER algorithms
    - Not trivial but not terrible (Section III A and B; kinda monte-carlo esque?)
    - Could you extrapolate between directed and undirected by applying a monte-carlo like acceptance criteria to ODER? interesting...
    - What if, instead of rank, you would only link to nodes that had a value close to you, and play with that tolerance?
    - What it, on top of that, you had some nodes that would act as "influencers"?
2. Replicate finding that the cluster size transition is discontinuous (Section IVA)
    - Reference 11 shows that this is true in the thermodynamic limit
    - They use that the jump happens with the addition of one edge length to say that it's discontinuous (I buy it)
    - They also have some nice discussion and a numerical analysis
2. Find the critical exponents..? i.e. can I replicate their results?
3. Investigate the rank-separation phenomena in the C-ODER process
