'''
Created on Jan 25, 2016

@author: spatel78745
'''

ewdFile = '/Users/spatel78745/py/tinyEWD.txt'

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
        self[edge.frm].append(edge)
        
        
    @classmethod
    def makeFromList(cls, edges):
        g = EdgeWeightedDigraph()
        for e in edges: g.addEdge(e)
        
        return g
    
    @classmethod
    def makeFromFile(cls, filename = ewdFile):
        with open(filename) as data:
            V = int(data.__next__())
            E = int(data.__next__())
            print('Reading', V, 'vertices and', E, 'edges', 'from', filename)
            
            g = EdgeWeightedDigraph()
            for line in data:
                tokens = line.split()
                g.addEdge((int(tokens[0]), int(tokens[1]), float(tokens[2])))
            
            return g
                
g = EdgeWeightedDigraph.makeFromFile()
print(g)