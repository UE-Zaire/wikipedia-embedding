import networkx as nx
import matplotlib.pyplot as plt


def draw(draw_graph):
    options = {
        'node_color': 'black',
        'node_size': 50,
        'line_color': 'grey',
        'linewidths': 0,
        'width': 0.1,
        'with_labels': True
    }
    nx.draw_spring(draw_graph, **options)
    plt.show()


pages = open('wikipedia-vital-3/pages list.txt', 'r')
links = open('wikipedia-vital-3/links.txt', 'r')

G = nx.Graph()

for p in pages:
    G.add_node(p.replace('\n', '').replace('-', '_'))

for line in links:
    s, t = line.replace('-', '_').replace('\n', '').split(',')
    if G.has_node(s) and G.has_node(t):
        G.add_edge(s, t)

print(G.edges())
print(nx.average_clustering(G))


for i in range(1):
    cut_edges = nx.minimum_edge_cut(G)
    print(cut_edges)
    for e in cut_edges:
        G.remove_edge(*e)

draw(G)
