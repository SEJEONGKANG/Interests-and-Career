"""
Main algorithm for RORO optimization
"""
import time
from utils import build_graph, compute_tree_and_distances, prepare_demand_info, initialize_score_matrix
from mip_optimizer_2 import optimize_allocation_with_blocking_costs
from solution_evaluator import evaluate_allocation
import util
import numpy as np
from collections import defaultdict
import networkx as nx
import gurobipy as gp
from gurobipy import Model, GRB, quicksum
from sklearn.cluster import AgglomerativeClustering
import math

def algorithm(prob_info, timelimit=60):
    """
    Main optimization algorithm for RORO
    
    Args:
        prob_info: Dictionary containing problem parameters
        timelimit: Time limit in seconds
        
    Returns:
        Best solution found
    """
    start_time = time.time()
    
    # Extract problem parameters
    N = prob_info['N']
    E = prob_info['E'] 
    K = prob_info['K']
    P = prob_info['P']
    F = prob_info['F']
    grid_graph = prob_info['grid_graph']
    
    # Build graph and compute distances
    G = build_graph(N, set(tuple(e) for e in E))
    T, distances = compute_tree_and_distances(G, N, F, grid_graph['nodes'])
    
    # Process demand information
    demand_info = prepare_demand_info(K)
    score_matrix = initialize_score_matrix(T, distances, N, len(K), F)
    T_nodes = [node for node,deg in T.degree() if deg ==1 ]

    count_dict = defaultdict(int)
    for node in T_nodes:
        path = nx.shortest_path(T, source=0, target=node)
        for p_n in path[1:]:
            count_dict[p_n] += 1
    no_node = [ n for n in count_dict if count_dict[n] >= int(len(T_nodes)/2)]
    no_node = no_node[:7]

    valid_nodes = [n for n in range(1,N) if n not in no_node]
    path_dict = defaultdict(list)    
    for node in valid_nodes:
        path = nx.shortest_path(T, source = 0, target= node)
        for idx, p_n in enumerate(path):
            if p_n not in no_node and p_n != 0:
                path_dict[node] = path[idx:]
                break
        
    nodes = list(path_dict.keys())
    path_sets = [set(path_dict[n]) for n in nodes]
    
    N1 = len(nodes)
    sim_matrix = np.zeros((N1, N1))
    
    for i in range(N1): 
        for j in range(N1): 
            if i == j: 
                sim_matrix[i, j] = 1 
            else: 
                inter = len(path_sets[i] & path_sets[j]) 
                union = len(path_sets[i] | path_sets[j]) 
                sim_matrix[i, j] = inter / union if union > 0 else 0


    dist_matrix = 1 - sim_matrix  # 거리 = 1 - 유사도
    clustering = AgglomerativeClustering(n_clusters=int(math.sqrt(N)), metric='precomputed', linkage='average')
    labels = clustering.fit_predict(dist_matrix)
    final_label = max(labels) + 1
    node_clusters = {nodes[i]: labels[i] for i in range(N1)}
 
    node_cluster = defaultdict(list)
    for node, label in node_clusters.items():
        node_cluster[label].append(node)

    node_cluster[final_label] = list(no_node)

    ################################################################
    ## optimization model
    ################################################################
    same_index = []
    for p in range(P):
        same_list = []
        for k in range(len(demand_info)):
            if (demand_info[k][0]<=p) and (demand_info[k][1]>p):
                same_list.append(k)
        same_index.append(same_list)
    
    conflict_pair = []
    for i in range(len(K)):
        for j in range(len(K)):
            if (demand_info[i][0] < demand_info[j][0])and (demand_info[i][1] < demand_info[j][1]) and (demand_info[j][0] < demand_info[i][1]):
                conflict_pair.append((i, j))

    #no_node_dict = defaultdict(int)
    no_node_pair = []
    for i in range(len(K)):
        #my_set = set()
        for j in range(len(K)):
            #일타일내
            if (demand_info[i][0] < demand_info[j][0]) and (demand_info[i][1] > demand_info[j][0]):
                #my_set.add(demand_info[j][0])
                no_node_pair.append((i,j))
            elif (demand_info[i][1] > demand_info[j][1]) and (demand_info[i][0] < demand_info[j][1]):
                no_node_pair.append((i,j))
                #my_set.add(demand_info[j][1])
        #no_node_dict[i] = len(my_set)
                
    m = Model('Optimizing path assignment')
    DD = range(len(K))
    CC = node_cluster.keys()
    Y = m.addVars(DD, CC, vtype=GRB.INTEGER, name='y')
    Z = m.addVars(DD, CC, vtype=GRB.BINARY, name='z')
    m.setObjective(quicksum(Y[k1,c]*Z[k2,c] for (k1,k2) in conflict_pair for c in CC)+quicksum(Y[k1,final_label]*demand_info[k2][2]*0.1 for (k1,k2) in no_node_pair), GRB.MINIMIZE)

    for d in DD:
        m.addConstr(quicksum(Y[d,c] for c in CC) == K[d][1])
    
    for item in same_index:
        for c in CC:
            m.addConstr(quicksum(Y[d,c] for d in item) <= len(node_cluster[c]))
    
    for d in DD:
        for c in CC:
            Y[d,c].LB = 0
            m.addConstr(Y[d,c] <= len(node_cluster[c])*Z[d,c])
            m.addConstr(Z[d,c] <= Y[d,c])

    m.setParam('OutputFlag', 0)
    m.setParam('TimeLimit', 20)
    #m.setParam('MIPGap', 0.1)
    m.optimize()

    initial_allocation = np.zeros((N, P))
    priority_K = sorted([[k]+demand_info[k].tolist() for k in range(len(K))], key=lambda x: (-x[2], x[1]))

    for demand in priority_K:
        k, O, D, _, _ = demand
        for c in CC:
            if Y[k,c].X > 0.5:
                for n in node_cluster[c]:
                    score_matrix[n,k] += 2*F
                Q = int(Y[k,c].X)
            
                status = np.where(initial_allocation[:, D] == 0)[0].tolist()
                check_node = np.where(np.sum(initial_allocation[:, O:D] == 0, axis=1) == (D - O))[0].tolist()
                subgraph = G.subgraph(set(status).union(set(check_node)))
                for n in check_node:
                    try:
                        path = nx.shortest_path(subgraph, source=n, target=0)
                    except nx.NetworkXNoPath:
                        score_matrix[n, k] -= F*0.5
                for _ in range(Q):
                    candidates = sorted([(i, score_matrix[i, k]) for i in range(N)], key=lambda x: x[1], reverse=True)
                    for node, _ in candidates:
                        if node != 0 and np.sum(initial_allocation[node, O:D]) == 0:
                            initial_allocation[node, O:D] = k + 1
                            break
                for n in node_cluster[c]:
                    score_matrix[n,k] -= 2*F
    
    # # # MIP optimization
    remaining_time = timelimit - (time.time() - start_time)

    optimized_allocation = optimize_allocation_with_blocking_costs(
        prob_info, demand_info, distances, G, T, remaining_time, initial_allocation
    )

    #visualize_allocation_over_ports(optimized_allocation, grid_graph)
    # Evaluate refined solution
    optimized_allocation, mip_score, mip_solution, rehandle_list, used_nodes, available_nodes = evaluate_allocation(optimized_allocation, prob_info, G, F, demand_info, distances, None)
    sorted_rehandle_demands = sorted(rehandle_list, key=lambda x: (-demand_info[x[2]][1], x[0], x[1]))
    revised_dict = defaultdict(list)
    for demand in sorted_rehandle_demands:
        p, n, idx = demand
        D = demand_info[idx][1]
        score_matrix = distances
        for pp in range(p,D):
            for node in used_nodes[pp]:
                score_matrix[node] -= F
        
        status = np.where(optimized_allocation[:, D] == 0)[0].tolist()
        subgraph = G.subgraph(set(status).union(set(available_nodes[p])))
        for a_n in available_nodes[p]:
            try:
                path = nx.shortest_path(subgraph, source=a_n, target=0)
            except nx.NetworkXNoPath:
                score_matrix[a_n] -= F
        
        candidates = sorted([(i, score_matrix[i]) for i in available_nodes[p]], key=lambda x: x[1], reverse=True)
        for node, _ in candidates:
            if node != 0 and np.sum(optimized_allocation[node, p:D]) == 0 and score_matrix[n]+F < score_matrix[node]:
                optimized_allocation[node, p:D] = idx+1
                revised_dict[p].append((n, node, idx))
                path = nx.shortest_path(T ,source=0, target=node)
                used_nodes[p].update(path)
                break
          
    for p in revised_dict:
        for prev, nxt, idx in revised_dict[p]:
            optimized_allocation[prev, p:demand_info[idx][1]] = 0          
    _, mip_score, mip_solution, rehandle_list, used_nodes, available_nodes = evaluate_allocation(optimized_allocation, prob_info, G, F, demand_info, distances, revised_dict)
              
    # print(f"MIP solution score: {mip_score}")
    # print(f"Time spent: {time.time() - start_time}")
    return mip_solution
    

if __name__ == "__main__":
    # You can run this file to test your algorithm from terminal.
    import json
    import os
    import sys
    import jsbeautifier

    def numpy_to_python(obj):
        if isinstance(obj, np.int64) or isinstance(obj, np.int32):
            return int(obj)  
        if isinstance(obj, np.float64) or isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
        raise TypeError(f"Type {type(obj)} not serializable")
    
    # Arguments list should be problem_name, problem_file, timelimit (in seconds)
    if len(sys.argv) == 4:
        prob_name = sys.argv[1]
        prob_file = sys.argv[2]
        timelimit = int(sys.argv[3])

        with open(prob_file, 'r') as f:
            prob_info = json.load(f)

        exception = None
        solution = None

        try:
            alg_start_time = time.time()
            # Run algorithm!
            solution = algorithm(prob_info, timelimit)
            alg_end_time = time.time()

            checked_solution = util.check_feasibility(prob_info, solution)

            checked_solution['time'] = alg_end_time - alg_start_time
            checked_solution['timelimit_exception'] = (alg_end_time - alg_start_time) > timelimit + 2 # allowing additional 2 second!
            checked_solution['exception'] = exception

            checked_solution['prob_name'] = prob_name
            checked_solution['prob_file'] = prob_file


            with open('results.json', 'w') as f:
                opts = jsbeautifier.default_options()
                opts.indent_size = 2
                f.write(jsbeautifier.beautify(json.dumps(checked_solution, default=numpy_to_python), opts))
                print(f'Results are saved as file results.json')
                
            sys.exit(0)

        except Exception as e:
            print(f"Exception: {repr(e)}")
            sys.exit(1)

    else:
        print("Usage: python myalgorithm.py <problem_name> <problem_file> <timelimit_in_seconds>")
        sys.exit(2)