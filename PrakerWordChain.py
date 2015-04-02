import sys, getopt

class Graph():
  alphadict = {}       # Dictionary mapping alphastring to a word instance
  sortedalphas = []    # Sorted list of alphastrings
  wordgraph = {}       # Alphastring to set of out edges
  sources = {}         # Alphastrings with no in edges
  sortedsources = {}   # Source alphastrings, sorted alphabetically
  visited = []         # Whether alphastring node has been visited in DFS
  best_depth = -1      # Track (globally) best depth seen so far on this explore
  word_chain = []      # Track (globally) word chain for this explore
  shortestword = 'AAAAAAAAAAAAAAAAAAA' # Track (globally) shortest word in set
  longestword = ''     # Track (globally) longest word in set

  def __init__(self):
    self.alphadict = {}
    self.sortedalphas = []
    self.wordgraph = {}
    self.sources = {}
    self.sortedsources = {}
    self.visited = []
    self.best_depth = -1
    self.word_chain = []
    self.shortestword = 'AAAAAAAAAAAAAAAA'
    self.longestword = ''

  def build(self, inputfile):
    words = [line.strip() for line in open(inputfile, 'r')]
    print 'Number of words: %ld.' % (len(words))

    for word in words:
      alpha = ''.join(sorted(word))
      if alpha not in self.alphadict:
        self.alphadict[alpha] = word
        if len(self.shortestword) > len(word):
          self.shortestword = word
        if len(self.longestword) < len(word):
          self.longestword = word
    self.sortedalphas = sorted(self.alphadict)
    print 'Number of unique alphabetic sequences: %ld.' % (len(self.alphadict))
    print 'Shortest word: %s (%d chars).' % (self.shortestword, len(self.shortestword))
    print 'Longest word: %s (%d chars).' % (self.longestword, len(self.longestword))
    print 'Longest possible path: %d (from a %d to %d word).' % \
      (len(self.longestword) - len(self.shortestword), len(self.shortestword), len(self.longestword))

    self.wordgraph = {}
    for x in self.alphadict:
      self.wordgraph[x] = set()  # Set of edges out of node x

    self.sources = {}  # Track sources (nodes which have no IN edges)
    for x in range(len(self.shortestword), len(self.longestword) + 1):
      self.sources[x] = []

    for term in self.alphadict:
      letters = sorted(term)
      prev_letter = ''
      num_added = 0
      for i in range(0, len(letters)):
        if letters[i] != prev_letter:  # Prevent removal of duplicate letters
          front = letters[0:i]
          back = letters[i+1:len(letters)]
          new_term = ''.join(front) + ''.join(back)
          if new_term in self.alphadict:
            self.wordgraph[new_term].add(term)
            num_added = num_added + 1
          prev_letter = letters[i]
      if num_added == 0:
        self.sources[len(term)].insert(0, term)
    for x in range(len(self.shortestword), len(self.longestword) + 1):
      self.sortedsources[x] = sorted(self.sources[x])
    print 'DAG built, number of source vertices:'
    for x in range(len(self.shortestword), len(self.longestword) + 1):
      print 'Words length %d: %ld.' % (x, len(self.sortedsources[x]))

  def explore(self, node, currentdepth):
    #print 'Explore %s (depth %d).' % (node, currentdepth)
    isdeeper = False
    self.visited[self.sortedalphas.index(node)] = currentdepth
    if currentdepth > self.best_depth:
      isdeeper = True
      self.best_depth = currentdepth
      self.word_chain[currentdepth] = node

    outedges = self.wordgraph[node]
    for x in outedges:
      deeperfound = False
      if 0 > self.visited[self.sortedalphas.index(x)]:
        deeperfound = self.explore(x, currentdepth + 1)
      if deeperfound:
        isdeeper = True
        self.word_chain[currentdepth] = node
    return isdeeper

  def findlongestchain(self):
    self.visited = [-1 for term in self.sortedalphas]
    self.best_depth = -1
    longestchain = len(self.longestword) - len(self.shortestword) + 1
    self.word_chain = ['' for x in range(0, longestchain)]
    max_depth = -1
    max_chain = ['' for x in range(0, longestchain)]

    for wordlength in range(len(self.shortestword), len(self.longestword) + 1):
      for term in self.sortedsources[wordlength]:
        self.word_chain[:] = ['' for x in range(0, longestchain)]
        self.best_depth = -1
        print 'Explore from \'%s\'.' % (term)
        self.explore(term, 0)

        if self.best_depth > max_depth:
          print 'New max depth! %d to %d' % (max_depth, self.best_depth)
          self.print_chain(self.best_depth, self.word_chain)
          max_depth = self.best_depth
          for x in range(0, len(self.word_chain)):
            max_chain[x] = self.word_chain[x]
          if max_depth >= (len(self.longestword) - len(self.shortestword)):
            break
        elif self.best_depth == max_depth:
          print 'Matching max depth %d' % (self.best_depth)
          self.print_chain(self.best_depth, self.word_chain)
        else:
          print 'Best depth found %d' % (self.best_depth)
      if max_depth >= (len(self.longestword) - len(self.shortestword)):
        break

    print 'Max depth: %d' % (max_depth+1)
    for x in range(0, max_depth + 1):
      print self.alphadict[max_chain[x]]

  def print_chain(self, depth, chain):
    print 'Chain depth: %d' % (depth+1)
    for x in range(0, depth+1):
      print '%s ==> %s' % (chain[x], self.alphadict[chain[x]])
    print '\n'

def main(argv):
  if len(sys.argv) != 3:
    print 'Usage: python %s -i <inputfile>' % argv[0]
    sys.exit(2)
  inputfile = ''
  try:
    opts, args = getopt.getopt(argv[1:], "hi:")
  except getopt.GetoptError:
    print 'Usage: python %s -i <inputfile>' % argv[0]
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Usage: python %s -i <inputfile>' % argv[0]
      sys.exit()
    elif opt == '-i':
      inputfile = arg
    else:
      print 'Unrecognized option \'%s\' : \'%s\'; disregarding.' % (opt, arg)

  if inputfile == '':
    print 'No inputfile identified, aborting.'
    sys.exit(1)

  graph = Graph()
  graph.build(inputfile)
  graph.findlongestchain()

if __name__ == '__main__':
  main(sys.argv)
  
