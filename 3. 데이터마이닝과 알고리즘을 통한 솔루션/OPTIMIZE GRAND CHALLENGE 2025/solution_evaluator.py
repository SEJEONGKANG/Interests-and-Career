"""
Solution evaluation and feasibility checking for RORO optimization
"""
import numpy as np
import networkx as nx
from collections import defaultdict
import util
from path_optimization_2 import find_optimal_unloading_paths, find_optimal_loading_paths

def evaluate_allocation(allocation, prob_info, G, F, demand_info, distances, revise_dict):
    """
    Evaluate the cost of a given allocation solution
    
    Args:
        allocation: car allocation matrix (N x P)
        prob_info: Problem information dictionary
        G: Graph representing the RORO ship
        F: Blocking penalty factor
        
    Returns:
        tuple: (objective_value, solution_dict) or (inf, None) if infeasible
    """
    solution = defaultdict(list)
    node_allocations = np.full(prob_info['N'], -1)
    rehandle_list = []
    used_nodes_dict = defaultdict(set)
    available_nodes_dict = defaultdict(list)
    
    for port in range(prob_info['P']):
        # Determine loading and unloading demands
        if port == 0:
            # First port: only loading
            mask_1 = (allocation[:, port] > 0)
            loading_demand = np.where(mask_1)[0]
            unloading_demand = []
        else:
            # Subsequent ports: both loading and unloading
            O = [k for k in range(len(demand_info)) if demand_info[k][0] == port]
            if len(O) > 0:
                loading_demand = np.concatenate([np.where(allocation[:, port] == (o+1))[0] for o in O])
            else:
                loading_demand = []
            D = [k for k in range(len(demand_info)) if demand_info[k][1] == port]
            unloading_demand = [n for n in G.nodes if node_allocations[n] in D]

        # Process unloading operations
        rehandling_unload = find_optimal_unloading_paths(
                solution, port, G, node_allocations, unloading_demand, allocation, F, demand_info
            )
        rehandling_load, demand_nodes = find_optimal_loading_paths(
                solution, port, G, node_allocations, loading_demand, allocation, F
            )
        
        # Combine all loading demands (rehandling + new cars)
        rehandling_demands = rehandling_unload + rehandling_load
        for node, idx in rehandling_demands:
            rehandle_list.append((port, node, idx))
            
        # rehandling_demands = sorted(rehandling_demands, key=lambda x: demand_info[x[1]][1], reverse=True)
        # revised_rehandling_demands = []
        plus_nodes = [n for n in G.nodes if node_allocations[n] == -1 and n != 0]
        available_nodes_dict[port] = [n for n in plus_nodes if nx.has_path(G.subgraph(plus_nodes+[0]), source=0, target=n)]
        if revise_dict:
            revised_rehandling_demands = []
            if len(revise_dict[port]) > 0:
                for node, idx in rehandling_demands:
                    found = False
                    for prev, nxt, _ in revise_dict[port]:
                        if prev == node:
                            revised_rehandling_demands.append((nxt, idx))
                            found = True
                            break                                
                    if found == False:
                        revised_rehandling_demands.append((node, idx))
            else:
                revised_rehandling_demands = rehandling_demands
                    
        else:
            revised_rehandling_demands = rehandling_demands

        all_loading_demands = revised_rehandling_demands + demand_nodes
        # Find shortest paths for all loading operations
        path_list = []
        for node, demand in all_loading_demands:
            available_nodes = [n for n in G.nodes if node_allocations[n] == -1 or n == node]
            subgraph = G.subgraph(available_nodes)
            
            try:
                length, path = nx.single_source_dijkstra(subgraph, source=0, target=node)
                path = [int(x) for x in path]
                path_list.append((length, path, demand))
            except nx.NetworkXNoPath:
                continue
        
        # Sort paths by length (longest first for better allocation)
        sorted_paths = sorted(path_list, key=lambda x: x[0], reverse=True)
        # Allocate cars to positions
        for item in sorted_paths:
            path = item[1]
            target_node = path[-1]
            demand_idx = item[2]
            solution[port].append([path, demand_idx])
            node_allocations[target_node] = demand_idx
        for path in solution[port]:
            used_nodes_dict[port].update(path[0])
    
    # Check feasibility and compute objective
    feasibility_result = util.check_feasibility(prob_info, solution)
    if feasibility_result["feasible"]:
        return allocation, feasibility_result["obj"], solution, rehandle_list, used_nodes_dict, available_nodes_dict
    else:
        return None, float('inf'), None, None, None, None