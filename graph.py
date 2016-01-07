'''
Created on Dec 31, 2015

@author: spatel78745
'''

class Digraph(dict):
    def __init__(self, filename=None):
        self.V = 0
        self.E = 0
        if filename is not None:
            self.filename = filename
            self.load()

    def addEdge(self, v, w):
        if v not in self: self[v] = []
        if w not in self: self[w] = []
        self[v].insert(0, w)
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
    

class SymGraph:
    def __init__(self, filename, delim = " "):
        self.nextIndex = 0;
        self.index = {}
        self.name = {}
        self.G = Graph()
        self.filename = filename
        self.delim = delim
        
        with open(self.filename) as gfile:
            for line in gfile:
                line.strip();
                vertices = line.split()
                
                s = vertices[0]
                self.mapVertex(s)
                for w in vertices[1:]:
                    self.mapVertex(w)
                    self.G.addEdge(self.index[s], self.index[w])
                
    def mapVertex(self, name):
        if name in self.index: return
        self.index[name] = self.nextIndex
        self.name[self.nextIndex] = name
        self.nextIndex += 1
        
    def toStr(self, adj):
        return ' '.join([ self.name[v] for v in adj ])
        
    def __str__(self):
        # Converts the adjacency list of vIndex to a string
        
        return '\n'.join([ '%s: %s' % (self.name [v], self.toStr(self.G.adj(v))) for v in self.G])
    
class DepthFirstSearch:
    def __init__(self, G, s):
        self.G = G
        self.marked = {}
        self.edgeTo = {}
        self.s = s
        self.visited = []
        
        for v in G:
            self.marked[v] = False
            self.edgeTo[v] = None
            
        self.dfs(G, s, s)
    
    def dfs(self, G, v, u):
        self.marked[v] = True
        self.visited.append(v)
        print('+%d visited: %s' % (v, self.visited))
        for w in G[v]:
            if not self.marked[w]: 
                self.edgeTo[w] = v
                self.dfs(G, w, v)
            elif w != u:
#                 idx = self.visited.index(w)
#                 cycle = self.visited[idx:] + [0]
#                 print('cycle:', cycle, u, v, w, idx)
                print('cycle')
        self.visited = self.visited[:-1]
        print('-%d visited: %s' % (v, self.visited))
            
    def hasPathTo(self, v): return self.marked[v]
    
    def pathTo(self, v):
#         print('edgeTo:', self.edgeTo)
#         print('marked:', self.marked)
#         print('hasPathTo:', self.hasPathTo(v), self.marked[v])
        path = []
        if not self.hasPathTo(v): return path
        while v != self.s:
            path.append(v)
            v = self.edgeTo[v]
             
        path.append(self.s)
        path.reverse()
        
        return path
    
class BreadthFirstSearch:
    def __init__(self, G, s):
        self.G = G
        self.edgeTo = {}
        self.s = s
        self.whileCount = 0
        
        self.marked = {}
        for v in G:
            self.marked[v] = False
            
        self.bfs(G, s)
        
    def _len(self, queue):
        self.whileCount += 1
        print('while:', self.whileCount, queue, len(queue))
        return len(queue)
    
    def bfs(self, G, v):
        self.marked[self.s] = True
        queue = [self.s]
        forCount = 0
        while self._len(queue) != 0:
            v = queue.pop(0)
#             print('chk', v, queue, self.edgeTo, self.marked)
            for w in G[v]:
                forCount += 1
                if not self.marked[w]:
                    self.edgeTo[w] = v
                    self.marked[w] = True
                    queue.append(w)
        print('forCount:', forCount)
            
    def hasPath(self, v): return v in self.G
    
    def pathTo(self, v):
        path = []
        while v != self.s:
            path.append(v)
            v = self.edgeTo[v]
            
        path.append(self.s)
        path.reverse()
        
        return path
    
# def testGraph():
# g = Graph()
# g.addEdge(0, 1)
# g.addEdge(1, 2)
# g.addEdge(0, 2)
# print(g, g.V, g.E)

def printPaths(search):
    g = search.G
    print('all paths in', g)
    for v in g:
        print(v, ':', search.pathTo(v))

def sedgeGraph():
    g = Graph()
    
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(0, 5)
    g.addEdge(1, 2)
    g.addEdge(2, 3)
    g.addEdge(2, 4)
    g.addEdge(3, 4)
    g.addEdge(3, 5)
    
    return g

def doBfs(g):
    bfs = BreadthFirstSearch(g, 0)
    for v in g:
        print(v, ':', bfs.pathTo(v))
        
def ex1():
    g = Graph()
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(1, 3)
    g.addEdge(2, 3)
    doBfs(g)

def ex2():
    g = Graph()
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(1, 3)
    g.addEdge(2, 3)
    g.addEdge(3, 4)
    doBfs(g)

def cycle1():
    g = Graph()
    g.addEdge(0, 1)
    g.addEdge(1, 2)
    dfs = DepthFirstSearch(g, 0)
    printPaths(dfs)
    
def cycle2():
    g = Graph()
    g.addEdge(0, 1)
    g.addEdge(1, 2)
    g.addEdge(2, 0)
    dfs = DepthFirstSearch(g, 0)
    printPaths(dfs)
    
def testSymGraph():
    sg = SymGraph('/Users/spatel78745/py/routes.txt')
    print('name: ', sg.name)
    print('index: ', sg.index)
    print('G:', sg.G)
    print(sg)
    
dg = Digraph('/Users/spatel78745/py/tinyDG.txt')
print('Adjacency Lists')
print(dg)
print('V=%d, E=%d' % (dg.V, dg.E))
#     print(sg.name)
#     print(sg.index)
    
# testSymGraph()
    
# cycle2()
    
# g1 = Graph('/Users/spatel78745/py/tinyG.txt')

# print(g1, g1.V, g1.E)
# g1 = sedgeGraph()
# 
# # print(g1)
# 
# print('BFS Shortest Paths')
# bfs = BreadthFirstSearch(g1, 0)
# for v in g1:
#     print(v, ':', bfs.pathTo(v))
    
# print('DFS Shortest Paths')
# dfs = DepthFirstSearch(g1, 0)
# for v in g1:
#     print(v, ':', dfs.pathTo(v))
    
if __name__ == '__main__':
    pass