'''
Created on Jan 25, 2016

@author: spatel78745
'''

EWD_FILE = '/Users/spatel78745/py/tinyEWD.txt'
EWDAG_FILE = '/Users/spatel78745/py/tinyEWDAG.txt'
POS_INF = 1000000

class Pq(dict):
    def contains(self, i): return i in self
    
    def change(self, i, val): self[i] = val
    
    insert = change
    
    def delMin(self):
        minIdx = min(zip(self.values(), self.keys()))[1]
        del(self[minIdx])
        
        return minIdx
    
    def empty(self): return len(self) == 0

class Edge(tuple):
    @property
    def frm(self): return self[0]
    
    @property
    def to(self): return self[1]
    
    @property
    def weight(self): return self[2]
    
class EdgeWeightedDigraph(dict):
    def addEdge(self, edge):
        edge = Edge(edge)
        if edge.frm not in self: self[edge.frm] = []
        if edge.to not in self: self[edge.to] = []
        self[edge.frm].append(edge)
        
    def adj(self, v): return self[v]
        
    @classmethod
    def makeFromList(cls, edges):
        g = EdgeWeightedDigraph()
        for e in edges: g.addEdge(e)
        
        return g
    
    @classmethod
    def makeFromFile(cls, filename = EWD_FILE):
        with open(filename) as data:
            V = int(data.__next__())
            E = int(data.__next__())
            print('Reading', V, 'vertices and', E, 'edges', 'from', filename)
            
            g = EdgeWeightedDigraph()
            for line in data:
                tokens = line.split()
                g.addEdge((int(tokens[0]), int(tokens[1]), float(tokens[2])))
            
            return g
        
    def vertices(self): return self.keys()
            
class DijkstraSP:
    def __init__(self, G, s):
        self.edgeTo = {}
        self.distTo = {}
        pq = Pq()
        
        for v in G.vertices():
            self.edgeTo[v] = None
            self.distTo[v] = POS_INF
            
        self.distTo[s] = 0.0
        pq.insert(s, 0.0)
        
        while not pq.empty(): self.relax(G, pq, pq.delMin())
        
    def relax(self, G, pq, v):
        for edge in G.adj(v):
            w = edge.to
            if self.distTo[w] > self.distTo[v] + edge.weight:
                self.distTo[w] = self.distTo[v] + edge.weight
                self.edgeTo[w] = v
                if pq.contains(w): pq.change(w, edge.weight)
                else: pq.insert(w, edge.weight)
                
    def pathTo(self, v):
        path = []
        if self.distTo[v] == POS_INF: return path
        
        while self.edgeTo[v] != None:
            path.append(v)
            v = self.edgeTo[v]
        path.append(v)
            
        return list(reversed(path))
    
class DirectedCycle:
    def __init__(self, G):
        self.marked = {}
        self.edgeTo = {}
        self.onStack = {}
        self.cycle = None
        
        for v in G.keys():
            self.marked[v] = False
            self.edgeTo[v] = None
            self.onStack[v] = False
            
        for v in G.keys():
            if not self.marked[v]: self.dfs(G, v)
            
    def hasCycle(self): return self.cycle is not None
            
    def dfs(self, G, v):
        self.onStack[v] = True
        self.marked[v] = True
        for edge in G.adj(v):
            w = edge.to
            if self.cycle is not None: return
            elif not self.marked[w]:
                self.edgeTo[w] = v
                self.dfs(G, w)
            elif self.onStack[w] is True:
                self.cycle = []
                x = v
                while x != w:
                    self.cycle.append(x)
                    x = self.edgeTo[x]
                self.cycle.append(w)
                self.cycle.append(v)
                self.cycle.reverse()
        self.onStack[v] = False;
        
class Topological:
    def __init__(self, G):
        self.reversePost = []
        self.marked = {}
        
        dc = DirectedCycle(G)
        if dc.hasCycle() is True: return 
        
        for v in G.keys():
            self.marked[v] = False
            
        for v in G.keys():
            if not self.marked[v]: self.dfs(G, v)
            
        self.reversePost.reverse()
            
    def dfs(self, G, v):
        self.marked[v] = True
        for edge in G.adj(v):
            w = edge.to
            if self.marked[w] is not True:
                self.dfs(G, w)
        self.reversePost.append(v);
        
class AcyclicSP:
    def __init__(self, G, s):
        self.distTo = {}
        self.edgeTo = {}
        self.s = s
        
        for v in G.vertices():
            self.edgeTo[v] = None
            self.distTo[v] = POS_INF
        self.distTo[s] = 0.0
            
        vertices = Topological(G).reversePost
        for v in vertices:
            self.relax(G, v)
            
    def relax(self, G, v):
        for edge in G.adj(v):
            w = edge.to
            if self.distTo[w] > self.distTo[v] + edge.weight:
                self.distTo[w] = self.distTo[v] + edge.weight
                self.edgeTo[w] = edge
                
    def hasPathTo(self, v): return self.edgeTo[v] is not None
    
    def pathTo(self, v):
        if not self.hasPathTo(v): return []
        
        path = []
        edge = self.edgeTo[v]
        path.append(edge)
        while edge.frm != self.s:
            edge = self.edgeTo[edge.frm]
            path.append(edge)
        path.reverse()
        
        return path
                    
# g = EdgeWeightedDigraph.makeFromList([(0,1,0.2), (1,2,0.4), (1,3,0.6), (2,3,0.8), (3,0,0.95])
# g = EdgeWeightedDigraph.makeFromList([(0,1,0.2), (1,2,0.4), (1,3,0.6), (2,3,0.8)])
# dc = DirectedCycle(g)
# print(dc.cycle)
# print(dc.hasCycle())
# 
# t = Topological(g)
# print(t.reversePost)

g = EdgeWeightedDigraph.makeFromFile(EWDAG_FILE)
asp = AcyclicSP(g, 5)
# t = Topological(g)
# print(t.reversePost)

# print(g)
# sp = DijkstraSP(g, 0)
# print(sp.edgeTo)
# print(sp.distTo)

