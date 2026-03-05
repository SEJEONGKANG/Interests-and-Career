"""
Demand processing and dependency analysis for car operations
"""
import numpy as np
from collections import defaultdict

def prepare_demand_info(K):
    """Convert demand data to structured format"""
    demand_info = np.zeros((len(K), 4), dtype=int)
    for idx, k in enumerate(K):
        demand_info[idx] = [k[0][0], k[0][1], k[1], 0]
    return demand_info


"""
Graph operations and utilities for RORO optimization
"""
import networkx as nx
from collections import defaultdict

def build_graph(N, E):
    """Build a graph from nodes and edges"""
    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(E)
    return G

def compute_tree_and_distances(G, N, F, grid_nodes):
    """Compute BFS tree and distances from root node"""
    T = nx.bfs_tree(G, source=0)
    distances = {attr['id']: len(nx.shortest_path(T, 0, attr['id'])) for _, attr in grid_nodes}
    return T, distances

def initialize_score_matrix(T, distances, N, K_len, F):
    T_nodes = [node for node,deg in T.degree() if deg ==1 ]
    score_matrix = np.zeros((N, K_len))
    for i in range(N):
        for k in range(K_len):
            score_matrix[i][k] = distances[i]
    # for k in advantage_dict:
    #     for i in advantage_dict[k]:
    #         score_matrix[i][k] += F
    return score_matrix