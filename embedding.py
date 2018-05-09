import networkx as nx
import matplotlib.pyplot as plt
from sklearn.manifold import spectral_embedding
from sklearn.cluster import spectral_clustering
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

NUM_CLUSTERS = 10


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

x = spectral_embedding(adj, n_components=2)
print(x)

clusters = spectral_clustering(adj, n_clusters=NUM_CLUSTERS)

fig, ax = plt.subplots()
print(x[:, 0])

for i, txt in enumerate(G.nodes_iter()):
    ax.text(*x[i], txt, fontdict={'alpha': 0.2}, zorder=1)

alpha = []
for i, (x0, x1) in enumerate(x):
    n = G.nodes()[i]
    if G.has_edge(n, 'Mathematics'):
        alpha.append(1)
    else:
        alpha.append(0.1)

viridis = plt.get_cmap('viridis')
cNorm = colors.Normalize(vmin=0, vmax=NUM_CLUSTERS - 1)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=viridis)

target = None

if target is not None:
    for i, (x0, x1) in enumerate(x):
        colorVal = list(scalarMap.to_rgba(clusters[i]))
        n = G.nodes()[i]
        if not G.has_edge(n, target) and not G.has_edge(target, n):
            colorVal[3] = 0.1
        ax.scatter(x0, x1, c=colorVal, zorder=2)
else:
    ax.scatter(x[:, 0], x[:, 1], c=clusters, zorder=2)

plt.show()

open('clusters%s.csv' % NUM_CLUSTERS, 'w').write('\n'.join(str(int(c)) for c in clusters))
np.savetxt('embedding.csv', x, delimiter=',')

