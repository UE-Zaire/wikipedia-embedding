import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import spectral_clustering


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

adj = nx.adjacency_matrix(G)

x = spectral_clustering(adj, n_clusters=50)
print(x)

final_G = nx.Graph()

for n in G.nodes_iter():
    final_G.add_node(n)

for a, b in G.edges_iter():
    i_a = G.nodes().index(a)
    i_b = G.nodes().index(b)
    if x[i_a] == x[i_b]:
        final_G.add_edge(a, b)

draw(final_G)
