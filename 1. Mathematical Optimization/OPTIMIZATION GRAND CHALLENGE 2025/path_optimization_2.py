"""
Path finding and optimization for car loading/unloading operations
"""
import networkx as nx
import numpy as np
from collections import defaultdict

def cost_function(u, v, begin_node, end_node, ignore_nodes, F, node_allocations):
    """Calculate cost for traversing an edge"""
    edge_cost = 1
    if (node_allocations[v] != -1 and 
        v != end_node and 
        v not in ignore_nodes):
        edge_cost += F
    return edge_cost


def unload_avoiding_blocking(solution, port, G, node_allocations, demand, unload_path):
    unhandled_demand = []
    demand = sorted(demand, key=lambda x: len(unload_path[x]))
    for node in demand:
        available_nodes = [n for n in G.nodes if node_allocations[n] == -1 or n == node]
        subgraph = G.subgraph(available_nodes)                
        try:
            length, path = nx.single_source_dijkstra(subgraph, source=node, target=0)
            path = [int(x) for x in path]
            solution[port].append([path, node_allocations[node]])
            node_allocations[node] = -1  # Mark as empty after unloading
            
        except nx.NetworkXNoPath:
            unhandled_demand.append(node)
    return unhandled_demand
    
def find_optimal_unloading_paths(solution, port, G, node_allocations, demand, initial_allocation, F, demand_info):
    """Find optimal paths for unloading cars"""
    rehandling_nodes = []
    unload_path = dict()
    remaining_demand = []
    final_rehandling_nodes = []
    ignore_nodes = []
    if len(demand) == 0:
        return final_rehandling_nodes
    
    for node in demand:
        available_nodes = [n for n in G.nodes if node_allocations[n] == -1 or n == node]
        subgraph = G.subgraph(available_nodes)                
        try:
            length, path = nx.single_source_dijkstra(subgraph, source=node, target=0)
            path = [int(x) for x in path]
            solution[port].append([path, node_allocations[node]])
            node_allocations[node] = -1  # Mark as empty after unloading
            
        except nx.NetworkXNoPath:
            remaining_demand.append(node)
            # Use full graph with blocking cost
            weight_func = lambda u, v, d: cost_function(
                u, v, node, 0, ignore_nodes, F, node_allocations
            )
            length, path = nx.single_source_dijkstra(
                G, source=node, target=0, weight=weight_func
            )
            path = [int(x) for x in path]
            unload_path[node] = path
            # Handle blocking cars
            for i in range(len(path)-1, 0, -1):
                if node_allocations[path[i]] != -1 and path[i] not in demand:
                    if path[i] not in rehandling_nodes:
                        rehandling_nodes.append(path[i])
                    ignore_nodes.append(path[i])
            ignore_nodes.append(node)

    for b_n in rehandling_nodes:
        idx = node_allocations[b_n]
        D = demand_info[idx][1]
        check_node = np.where(np.sum(initial_allocation[:, port:D] == 0, axis=1) == (D - port))[0].tolist()
        check_node = [n for n in check_node if node_allocations[n] == -1]
        available_nodes = [ n for n in G.nodes if node_allocations[n] == -1 or n == b_n]
        candidates = [n for n in check_node if nx.has_path(G.subgraph(available_nodes), source=b_n, target=n) and n!=0]
        no_node = set()
        for r_d in remaining_demand:
            no_node.update(unload_path[r_d])
        candidates = [n for n in candidates if n not in no_node]
        if len(candidates) > 0:
            path = nx.shortest_path(G.subgraph(available_nodes), source=b_n, target = candidates[-1])
            solution[port].append([path, idx])
            node_allocations[b_n] = -1
            node_allocations[candidates[-1]] = idx
        else:
            path = nx.shortest_path(G.subgraph(available_nodes), source=b_n, target=0)
            solution[port].append([path, idx])
            node_allocations[b_n] = -1
            final_rehandling_nodes.append((b_n, idx))
        
        remaining_demand = unload_avoiding_blocking(solution, port, G, node_allocations, remaining_demand, unload_path)
    return final_rehandling_nodes

def find_optimal_loading_paths(solution, port, G, node_allocations, demand, initial_allocation, F):
    """Find optimal paths for loading cars"""
    demand_nodes = []
    rehandling_nodes = []
    
    for node in reversed(demand):  # Process in reverse order
        demand_nodes.append((node, initial_allocation[node, port] - 1))
        
        # Try path with only available nodes
        available_nodes = [n for n in G.nodes if node_allocations[n] == -1]
        subgraph = G.subgraph(available_nodes)
        
        try:
            length, path = nx.single_source_dijkstra(subgraph, source=0, target=node)
            
        except nx.NetworkXNoPath:
            # Use full graph with blocking cost
            weight_func = lambda u, v, d: cost_function(
                u, v, 0, node, [], F, node_allocations
            )
            length, path = nx.single_source_dijkstra(
                G, source=0, target=node, weight=weight_func
            )
            path = [int(x) for x in path]
            
            # Handle blocking cars
            for i in range(len(path) - 1):
                if node_allocations[path[i]] != -1:
                    solution[port].append([path[:i+1][::-1], node_allocations[path[i]]])
                    rehandling_nodes.append((path[i], node_allocations[path[i]]))
                    node_allocations[path[i]] = -1
    
    return rehandling_nodes, demand_nodes