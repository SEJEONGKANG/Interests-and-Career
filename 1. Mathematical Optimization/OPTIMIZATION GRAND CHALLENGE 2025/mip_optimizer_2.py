"""
Mixed Integer Programming optimization for car allocation refinement
"""
import numpy as np
from collections import defaultdict
from gurobipy import Model, GRB, quicksum
import networkx as nx

def optimize_allocation_with_blocking_costs(prob_info, demand_info, distances, G, T, timelimit, base_allocation):
    """
    Refine allocation using MIP with explicit blocking cost modeling
    
    Args:
        base_allocation: Initial allocation matrix
        prob_info: Problem information
        demand_info: Demand specifications
        distances: Distance matrix
        G: Graph object
        T: Tree object
        timelimit: Time limit for optimization
        
    Returns:
        Optimized allocation matrix
    """
    N, P, F = prob_info['N'], prob_info['P'], prob_info['F']
    K = len(demand_info)
    
    # Build path dependencies using the tree
    edge_list = []
    for node in range(1, N):
        path = nx.shortest_path(T, source=0, target=node)
        for idx in range(len(path)-2):
            edge_list.append((path[idx+2], path[idx+1]))

    # Build port-based demand groups
    same_index = []
    load_dict = defaultdict(set)
    unload_dict = defaultdict(set)
    stay_dict = defaultdict(set)
    
    for p in range(P):
        # cars present at port p
        same_list = []
        for k in range(K):
            if (demand_info[k][0] <= p) and (demand_info[k][1] > p):
                same_list.append(k)
        same_index.append(same_list)
        
        # cars moving at port p
        load_dict[p] = set([k for k in range(K) 
                       if (demand_info[k][0] == p)])
        unload_dict[p] = set([k for k in range(K) if demand_info[k][1] == p])
        
        # cars staying through port p  
        stay_dict[p] = set([k for k in range(K) 
                       if (demand_info[k][0] < p) and (demand_info[k][1] > p)])
    
    # Create MIP model
    m = Model('Allocation Optimization with Blocking Costs')
    
    # Decision variables
    KK = range(K)
    NN = range(1, N) 
    PP = range(1, P-1)
    
    # X[k,n]: Binary, car type k assigned to node n
    X = m.addVars(KK, NN, vtype=GRB.BINARY, name='car_assignment')
    
    # Y[n,p]: Binary, node n causes blocking at port p
    Y = m.addVars(NN, PP, vtype=GRB.CONTINUOUS, name='blocking_indicator')
    
    # Z[n,p]: Binary, node n has cars moving at port p in its subtree
    Z = m.addVars(NN, PP, vtype=GRB.CONTINUOUS, name='movement_indicator')
    
    # A[n,p]: Binary, node n has cars staying at port p
    A = m.addVars(NN, PP, vtype=GRB.CONTINUOUS, name='staying_indicator')
    
    # Objective: Minimize blocking cost + distance cost
    blocking_cost = F * quicksum(Y[n, p] for n in NN for p in PP)
    distance_cost = quicksum(X[k, n] * distances[n] for k in KK for n in NN)
    
    m.setObjective(2*blocking_cost+2*distance_cost, GRB.MINIMIZE)

    initial_X = np.zeros((len(KK), N))
    for n in NN:
        for k in KK:
            if np.any(base_allocation[n,:]== k+1):
                initial_X[k,n] = 1

    for k in KK:
        for n in NN:
            X[k,n].Start = initial_X[k,n]
            X[k,n].BranchPriority = 100
        
    # Constraints
    # 1. Demand satisfaction
    for k in KK:
        m.addConstr(quicksum(X[k, n] for n in NN) == demand_info[k][2])
    
    # 2. Node capacity (one car type per node per time period)
    for item in same_index:
        for n in NN:
            m.addSOS(GRB.SOS_TYPE1, [X[k, n] for k in item])
    
    # 3. Blocking logic
    for p in PP:
        #m.addConstr(quicksum(Y[n1,p] for n1 in NN) <= 40)
        for (n1, n2) in edge_list:
            m.addConstr(Z[n1,p] <= Z[n2,p])
        for n1 in NN:
            A[n1,p].UB = 1
            A[n1,p].LB = 0
            Z[n1,p].UB = 1
            Z[n1,p].LB = 0
            Y[n1,p].UB = 1
            Y[n1,p].LB = 0
            # A node has staying cars if any stay-type cars are assigned
            m.addConstr(A[n1,p] == quicksum(X[k, n1] for k in stay_dict[p]))
            # A node has movement in subtree if any move-type cars in subtree
            m.addConstr(Z[n1,p] >= quicksum(X[k,n1] for k in load_dict[p]))
            m.addConstr(Z[n1,p] >= quicksum(X[k,n1] for k in unload_dict[p]))
            # Blocking occurs when both conditions are met
            m.addConstr(Y[n1,p] <= Z[n1,p])
            m.addConstr(Y[n1,p] <= A[n1,p])
            m.addConstr(Y[n1,p] >= Z[n1,p] + A[n1,p] -1 )
   
    # Solver parameters
    m.setParam('TimeLimit', timelimit - 6)
    m.setParam('OutputFlag', 0)
    m.optimize()
    # Extract solution
    optimized_allocation = np.zeros((N, P), dtype=int)
    if m.SolCount > 0:
        for n in NN:
            for k in KK:
                if X[k, n].X > 0.5:
                    O = demand_info[k][0]
                    D = demand_info[k][1]
                    optimized_allocation[n, O:D] = k + 1
        # for p in PP:
        #     rehandle_count = 0
        #     rehandle_node = []
        #     print('---------port', p, '---------')
        #     for n in NN:
        #         if Y[n,p].X > 0.5:
        #             rehandle_count += 1
        #             rehandle_node.append(n)

        #     print('rehandle_count', rehandle_count, rehandle_node)
    return optimized_allocation