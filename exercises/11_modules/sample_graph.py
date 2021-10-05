# import module
from graphviz import Digraph

# instantiating object
dot = Digraph(comment='A Round Graph')

# Adding nodes
dot.node('A', 'Alex')
dot.node('B', 'Rishu')
dot.node('C', 'Mohe')
dot.node('D', 'Satyam')

# Adding edges
dot.edges(['AB', 'AC', 'AD'])
dot.edge('B', 'C', constraint = 'false')
dot.edge('C', 'D',headlabel='e0/1', taillabel='e0/2', label=' '*12, constraint = 'false')

# saving source code

dot.render('Graph', view = True)


