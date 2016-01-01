'''
Created on Dec 31, 2015

@author: spatel78745
'''


class Graph(dict):
    def __init__(self, filename=None):
        self.V = 0
        self.E = 0
        if filename is not None:
            self.filename = filename
            self.load()
    
    def addEdge(self, v, w):
        if v not in self: self[v] = []
        if w not in self: self[w] = []
        self[v].append(w)
        self[w].append(v)
        self.E += 1
        
    def load(self):
        with open(self.filename) as gdata:
            self.V = int(gdata.__next__())
            E = int(gdata.__next__())
            print('Reading', self.V, 'vertices and', E, 'edges', 'from',
                  self.filename)
            for edge in gdata:
                vertices = edge.split()
                self.addEdge(int(vertices[0]), int(vertices[1]))
                
    def adj(self, v): return self[v]
    
class DepthFirstSearch:
    def __init__(self, G, s):
        self.G = G
        self.count = 0
        self.marked = {}
        self.dfs(G, s)
    
    def dfs(self, G, v):
        self.marked[v] = True
        for w in G[v]:
            if w not in self.marked: self.dfs(G, w)

# def testGraph():
# g = Graph()
# g.addEdge(0, 1)
# g.addEdge(1, 2)
# g.addEdge(0, 2)
# print(g, g.V, g.E)

g1 = Graph('/Users/spatel78745/py/tinyG.txt')
# print(g1, g1.V, g1.E)

# print('Vertices adjacent to 0')
# for v in g1.adj(0):
#     print(v)

print('Searching: ', g1)    
search = DepthFirstSearch(g1, 9)
print('Vertices connected to', 9, ':', search.marked.keys())    
    
# testGraph()

if __name__ == '__main__':
    pass