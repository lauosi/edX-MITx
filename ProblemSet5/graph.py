# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight1, weight2):
        Edge.__init__(self, src, dest)
        self.weight1 = weight1
        self.weight2 = weight2
        
    def getTotalDistance(self):
        return self.weight1
        
    def getOutdoorDistance(self):
        return self.weight2
        
    def __str__(self):
        return '{0}->{1} ({2}, {3})'.format(self.src.getName(),self.dest.getName(), self.getTotalDistance(), self.getOutdoorDistance())

class WeightedDigraph(Digraph):
    def __init__(self):
        Digraph.__init__(self)
    
    def addEdge(self, weighted_edge):
        src = weighted_edge.getSource()
        dest = weighted_edge.getDestination()
        weight1 = float(weighted_edge.getTotalDistance())
        weight2 = float(weighted_edge.getOutdoorDistance())
        
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')

        self.edges[src].append([dest, (weight1, weight2)])
        
    def childrenOf(self, node):
        dest = [lst for value in self.edges[node] for lst in value if isinstance(lst, Node)]
        return dest   

    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2} ({3}, {4})\n'.format(res, k, d[0], d[1][0], d[1][1])
        return res[:-1]
        
