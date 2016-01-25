'''
Created on Jan 15, 2016

@author: spatel78745
'''

from functools import *

class Graph(dict):
    def __init__(self, edges=[]):
        for e in edges:
            self.addEdge(e[0], e[1], e[2]) 
    
    def addEdge(self, v, w, weight):
        if v not in self: self[v] = []
        if w not in self: self[w] = []
        self[v].append((w, weight))
        self[w].append((v, weight))
        
class Digraph(Graph):
    def addEdge(self, v, w, weight):
        if v not in self: self[v] = []
        if w not in self: self[w] = []
        self[v].append((v, w, weight))

def crossEdges(g, a, b):
    ce = []
    for v in a:
        for u in b:
            for e in g[v]:
                if e[0] == u:
                    ce.append((v, u, e[1]))
    return ce

def lightestEdge(edges):
    lightest = edges[0]
    for e in edges:
        if e[2] < lightest[2]: lightest = e
        
    return lightest
        
def mst(g):
    nt = list(g.keys())
    t = [ nt.pop() ]
    mstEdges = []
    print('Start tree %s !tree %s' % (t, nt))
    
    while nt:
        le = lightestEdge(crossEdges(g, t, nt))
        nt.remove(le[1])
        t.append(le[1])
        mstEdges.append(le)
        
    return mstEdges

INF = 9999

def sp(g, s):     
    edges = reduce(lambda x, y: x + y, g.values())
    
    distTo = { v:INF for v in g.keys()  }
    distTo[s] = 0
    edgeTo = { v:None for v in g.keys() }
    
    print('distTo', distTo)
    
    def relax(edge):
        v = edge[0]
        w = edge[1]
        weight = edge[2]
        if distTo[w] > distTo[v] + weight:
            distTo[w] = distTo[v] + weight
            edgeTo[w] = v
            print("relaxed %s, distance to %d = %d, parent is %d" % (edge, w, distTo[w], edgeTo[w]))
            return True
        
        return False
    
    def relaxAll(edges):
        count = 0;
        for e in edges:
            if relax(e): count += 1
            
        print("relaxed", count, "edges in this pass")
        return count != 0 
        
    while relaxAll(edges): pass
    
    print("distances", distTo)
    print("tree", edgeTo)
                
# g = Graph( [ (0, 2, 7), (0, 1, 3), (2, 4, 5), (2, 3, 1), (3, 4, 8), (3, 5, 4),
#             (4, 7, 11), (5, 6, 9), (6, 7, 2), (7, 8, 13) ] )
g = Digraph( [ (0,1,4), (1,2,6), (2,3,5), (2,4,1), (4,3,2) ] )
sp(g, 0)

# print(mst(g))