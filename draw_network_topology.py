import graphviz as gv
styles = {
    'graph': {
        'label': 'Network Map',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'box',
        'fontcolor': 'white',
        'color': '#006699',
        'style': 'filled',
        'fillcolor': '#006699',
        'margin': '0.4',
    },
    'edges': {
        'style': 'dashed',
        'color': 'green',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '14',
        'fontcolor': 'white',
    }
}

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

def draw_topology(topology_dict, output_filename='img/topology_new'):
    nodes = set([key[0] for key in (list(topology_dict.keys()) +list( topology_dict.values()))])
    g1 = gv.Graph(format='svg')
    for node in nodes:
        g1.node(node)

    for key, value in topology_dict.items():
        head, t_label = key
        tail, h_label = value
        g1.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" "*12)
        # headport='nw' tailport='s'
    g1 = apply_styles(g1, styles)

    print(g1.source)
    filename = g1.render(filename=output_filename,view=True)
    print ("Graph saved in {}".format(filename))

if __name__ == "__main__":
    diag6 ={
        ('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
        ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
        ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
        ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
        ('R3', 'Eth0/1'):('R4', 'Eth0/0'),
        ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
        ('SW1', 'Eth0/5'):('R6', 'Eth0/1')
        }
    draw_topology(diag6,'img/topo_1')
