'''
input: adjacency matrix of edges, nxn matrix
output: connected components,list of tuples
desired outpu: array of node values with cluster it's in (like HK)
'''
'''A recursive function that find finds and prints strongly connected
components using DFS traversal
u --> The vertex to be visited next
disc[] --> Stores discovery times of visited vertices
low[] -- >> earliest visited vertex (the vertex with minimum
            discovery time) that can be reached from subtree
            rooted with current vertex
st -- >> To store all the connected ancestors (could be part
       of SCC)
stackMember[] --> bit/index array for faster check whether
              a node is in stack
'''
# Runs this for each vertex
def SCCUtil(self,u,low,disc,stackMember,st):

    # Initialize discovery time and low value
    disc[u] = self.Time
    low[u] = self.Time
    self.Time += 1
    stackMember[u] = True
    st.append(u)

    # Go through all vertices adjacent to this
    for v in self.graph[u]:
        # If v is not visited yet, then recur for it
        if disc[v] == -1 :
            self.SCCUtil(v, low, disc, stackMember, st)
            # Check if the subtree rooted with v has a connection to
            # one of the ancestors of u
            # Case 1 (per above discussion on Disc and Low value)
            low[u] = min(low[u], low[v])
        elif stackMember[v] == True:
            '''Update low value of 'u' only if 'v' is still in stack
            (i.e. it's a back edge, not cross edge).
            Case 2 (per above discussion on Disc and Low value) '''
            low[u] = min(low[u], disc[v])
    # head node found, pop the stack and print an SCC
    w = -1 #To store stack extracted vertices
    if low[u] == disc[u]:
        while w != u:
            w = st.pop()
            print w,
            stackMember[w] = False

#The function to do DFS traversal.a
# It uses recursive SCCUtil()
def SCC(self):
    # Mark all the vertices as not visited
    # and Initialize parent and visited,
    # and ap(articulation point) arrays
    disc = [-1] * (self.V)
    low = [-1] * (self.V)
    stackMember = [False] * (self.V)
    st =[]
    # Call the recursive helper function
    # to find articulation points
    # in DFS tree rooted with vertex 'i'
    for i in range(self.V):
        if disc[i] == -1:
            self.SCCUtil(i, low, disc, stackMember, st)

def tarjan_change(edges):
        index_counter = [0]
        index = {}
        lowlink = {}
        stack = []
        component_list = []

        # v is node-- wait, but shouldn't it actually be u...?
        def calc_component(node):
            # v.index, v.lowlink
            index[node] = index_counter[0]
            lowlink[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)

            # find the children
            children = np.where(edges[node]>0)[0]
            if children == []: pass
            else:
                for child in children:
                    # if the child hasn't been visited, run this on it
                    if child not in lowlink:
                        # check if the subtree at child has a connection to one of the ancestors of node
                        calc_component(child)
                        lowlink[node] = min(lowlink[node],lowlink[child])
                    # update ancestors of node only if child is in the stack, e.g. is a back edge
                    elif child in stack:
                        lowlink[node] = min(lowlink[node],index[child])

            if lowlink[node]==index[node]:
                connected_component = []
                while True:
                    successor = stack.pop()
                    connected_component.append(successor)
                    if successor == node: break
                component_list.append(tuple(connected_component))

        for node in range(edges.shape[0]):
            if node not in lowlink:
                calc_component(node)

        return component_list
