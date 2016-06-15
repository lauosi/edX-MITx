# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph2 import * 

#
# Problem 2: Building up the Campus Map
#
     
def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    maps = open(mapFilename, 'r')
    gd = WeightedDigraph()

    for line in maps:
        new_line = line.split(' ', 4)
        
        try:
            gd.addNode(Node(str(new_line[0])))
        except:
            pass
        try:
            gd.addNode(Node(str(new_line[1])))
        except:
            pass 
        gd.addEdge(WeightedEdge(Node(str(new_line[0])), Node(str(new_line[1])), float(new_line[2]), float(new_line[3])))
        
   
    maps.close()
    return gd 
   
mitMap = load_map(r'C:\Users\Laura\Dropbox\MIT\ProblemSet5\ProblemSet5\mit_map.txt')        

#print mitMap.childrenOf(Node('32'))
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def calculateDistance(diagraph, path):
    total = 0
    outdoors = 0
    
    for node in path[:-1]:
        for value in diagraph.edges[node]:
            if value[0] == path[path.index(node) + 1]:
                total += value[1][0]
                outdoors += value[1][1]
    return (total, outdoors)
        
def ifValid(diagraph, path, maxTotalDist, maxDistOutdoors):
    
    distances = calculateDistance(diagraph, path)
    
    if distances[0] <= maxTotalDist and distances[1] <= maxDistOutdoors:
        return True
    else:
        return False

#print calculateDistance(mitMap, [Node('32'), Node('66'), Node('56')])
         
def DFS(digraph, start, end, maxTotalDist,maxDistOutdoors, path=[]): 
    
    path = path + [start]
    if start == end:
        if ifValid(digraph, path, maxTotalDist, maxDistOutdoors):
            return [path]
    paths = []
    for node in digraph.childrenOf(start):
        if node not in path: 
            newpaths = DFS(digraph, node, end, maxTotalDist,maxDistOutdoors, path)
            if newpaths != None:    
                    for newpath in newpaths:
                        paths.append(newpath) 
    return paths 
 

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    shortestDistance = 0.0
    shortestPath = []
    
    start = Node(start)
    end = Node(end)
    
    validPaths = DFS(digraph, start, end, maxTotalDist, maxDistOutdoors, path = [])
    
    if validPaths == []:
        raise ValueError
    
    for path in validPaths:
        
        dist = calculateDistance(digraph, path)
        
        if shortestDistance == 0.0:
            shortestDistance = dist[0]
            shortestPath = path
        else:
            if shortestDistance > dist[0]:
                shortestDistance = dist[0]
                shortestPath = path
    
    for i in range(len(shortestPath)):
        shortestPath[i] = shortestPath[i].getName()              
    return shortestPath
                
#print bruteForceSearch(mitMap, '32', '56', 200.0, 100.0)        
        
def shortestDFS(digraph, start, end, maxTotalDist,maxDistOutdoors, path=[], shortest = None): 
    start = Node(start)
    end = Node(end)
    
    path = path + [start]
    if start == end:
        print path
        if ifValid(digraph, path, maxTotalDist, maxDistOutdoors):
            if shortest == None or (calculateDistance(digraph, path)[0] < calculateDistance(digraph, shortest)[0]):
                return path
    
          
    for node in digraph.childrenOf(start):
        if node not in path:
            if shortest == None or (calculateDistance(digraph, path)[0] < calculateDistance(digraph, shortest)[0]):
                newPath = shortestDFS(digraph,node,end,maxTotalDist,maxDistOutdoors,path,shortest)
                if newPath != None:
                    shortest = newPath
                    print "Shortest :" + str(shortest)
    return shortest        
    
#print DFSShortest(mitMap,'32','56') 
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    shortest = shortestDFS(digraph, start, end, maxTotalDist,maxDistOutdoors, path=[], shortest = None)
    if shortest == None:
        raise ValueError
    for i in range(len(shortest)):
        shortest[i] = shortest[i].getName()
    return shortest


