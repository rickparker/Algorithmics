import sys, getopt

class Graph():

  nodes = []    # Sorted list of node IDs
  graph = {}    # Node ID to set of out edges (adjacency list)
  graph_rev = {}  # Node ID to set of out edges, representing reversal of graph
  visited = []  # Whether node has been visited in DFS
  clock = 0
  posttimes = []
  
  def __init__(self):
    sys.setrecursionlimit(100000)
    self.nodes = []
    self.graph = {}
    self.graph_rev = {}
    self.visited = []
    self.clock = 0
    self.posttimes = []

  def build(self, inputfile):
    edges = [line.strip() for line in open(inputfile, 'r')]
    num_edges = len(edges)

    last_edge = edges[-2]
    fromto = last_edge.split('\t')
    max_node = max(int(fromto[0]), int(fromto[1]))

    # Initialize data structures
    for x in range(0, max_node + 1):
      self.graph[x] = []
      self.nodes.append(x)
      self.graph_rev[x] = []
    
    for edge in edges:
      fromto = edge.split('\t')
      source = int(fromto[0])
      dest = int(fromto[1])
      self.graph[source].append(dest)
      self.graph_rev[dest].append(source)

  def DFS_PostTimesOnRev(self):
    self.visited = [False for x in self.nodes]
    self.posttimes = [-1 for x in self.nodes]
    
    for x in self.nodes:
      if not self.visited[x]:
        self.explore_PostTimesOnRev(x, 0)

  def explore_PostTimesOnRev(self, node, depth):
    self.visited[node] = True
    outedges = self.graph_rev[node]
    for x in outedges:
      if not self.visited[x]:
        self.explore_PostTimesOnRev(x, depth + 1)
    self.posttimes[self.clock] = node
    self.clock = self.clock + 1

  def findLargestSCC(self):
    results = set()
    num_edges = 0

    # Graph reversal built when graph built - don't need to reverse again
    # Generate posttimes by DFS'ing on Reversed Graph
    self.DFS_PostTimesOnRev()
    self.visited = [-1 for x in self.nodes]
    # Run explore() on vertex with highest posttime #
    for node in self.posttimes[::-1]:
      if self.visited[node] == -1:  # not visited
        (set_visited, num_edges_viewed) = self.explore_gather(node, node)
        print('SCC identified: %s, %ld edges.' % (repr(set_visited), num_edges_viewed))
        if len(set_visited) > len(results):
          print('Replacing as largest SCC so far.')
          results = set_visited
          num_edges = num_edges_viewed

    print('Max SCC: %ld nodes and %ld edges' % (len(results), num_edges))
    file_object = open('output.txt', 'w')
    file_object.write('Max SCC: %ld nodes and %ld edges' % (len(results), num_edges))
    file_object.write(repr(results))

  def explore_gather(self, node, label):  # return tuple (nodes visited, number edges)
    self.visited[node] = label
    visited_nodes = set()
    visited_nodes.add(node)
    outedges = self.graph[node]
    examined_edges = 0
    for x in outedges:
      if self.visited[x] == -1:  # not visited
        examined_edges = examined_edges + 1
        (set_visited, num_edges) = self.explore_gather(x, label)
        visited_nodes = visited_nodes.union(set_visited)
        examined_edges = examined_edges + num_edges
      elif self.visited[x] == label:  # edge to node visited during this run
        examined_edges = examined_edges + 1
    return (visited_nodes, examined_edges)

def main(argv):
  if len(sys.argv) != 3:
    print('Usage: python %s -i <inputfile>' % argv[0])
    sys.exit(2)
  inputfile = ''
  try:
    opts, args = getopt.getopt(argv[1:], "hi:")
  except getopt.GetoptError:
    print('Usage: python %s -i <inputfile>' % argv[0])
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('Usage: python %s -i <inputfile>' % argv[0])
      sys.exit()
    elif opt == '-i':
      inputfile = arg
    else:
      print('Unrecognized option \'%s\' : \'%s\'; disregarding.' % (opt, arg))

  if inputfile == '':
    print('No inputfile identified, aborting.')
    sys.exit(1)

  graph = Graph()
  graph.build(inputfile)
  print('Graph built, identifying SCCs.')
  graph.findLargestSCC()

if __name__ == '__main__':
  main(sys.argv)
