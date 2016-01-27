'''
Created on Jan 25, 2016

@author: spatel78745
'''
from pathlib import Path

EWD_FILE = '/Users/spatel78745/py/tinyEWD.txt'
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
        
    def vertices(self): return g.keys()
            
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
                
g = EdgeWeightedDigraph.makeFromFile()
print(g)
sp = DijkstraSP(g, 0)
print(sp.edgeTo)
print(sp.distTo)

