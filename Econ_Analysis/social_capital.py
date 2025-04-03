import networkx as nx
import matplotlib.pyplot as plt
import random

# 1. Create two highly connected clusters (cliques)
G = nx.Graph()

# Cluster 1: Nodes 1-10
cluster1_nodes = range(1, 11)
G.add_nodes_from(cluster1_nodes)
for i in cluster1_nodes:
    for j in cluster1_nodes:
        if i != j:
            G.add_edge(i, j)  # Fully connected within cluster 1

# Cluster 2: Nodes 11-20
cluster2_nodes = range(11, 21)
G.add_nodes_from(cluster2_nodes)
for i in cluster2_nodes:
    for j in cluster2_nodes:
        if i != j:
            G.add_edge(i, j)  # Fully connected within cluster 2

# 2. Create a weak connection between the clusters (a single, thin edge)
# Randomly select one node from each cluster to connect
node_from_cluster1 = random.choice(list(cluster1_nodes))
node_from_cluster2 = random.choice(list(cluster2_nodes))
G.add_edge(node_from_cluster1, node_from_cluster2, weight=0.1) # add weight for visualizing the edge

# 3. Visualize the graph
pos = nx.spring_layout(G, seed=42)  # Seed for reproducibility

# Draw nodes
nx.draw_networkx_nodes(G, pos, nodelist=cluster1_nodes, node_color="skyblue", label="Cluster 1")
nx.draw_networkx_nodes(G, pos, nodelist=cluster2_nodes, node_color="lightgreen", label="Cluster 2")

# Draw edges, making the weak connection thinner
edges = G.edges()
weights = [G[u][v]['weight'] if 'weight' in G[u][v] else 1 for u, v in edges] # default weight is 1 if not specified

nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights)

# Draw labels (optional)
#nx.draw_networkx_labels(G, pos, font_size=8)

#Add Legend
plt.legend(loc='upper left')

# Customize plot
plt.title("Two Highly Connected Clusters with a Weak Link")
plt.axis("off")  # Turn off axis labels

# 4. Display the plot
plt.show()