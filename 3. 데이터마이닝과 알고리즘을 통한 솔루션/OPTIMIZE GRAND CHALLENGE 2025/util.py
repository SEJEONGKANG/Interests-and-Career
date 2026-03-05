# util.py
# This file contains utility functions for checking the feasibility of solutions
# Last updated: 2025/07/05

import numpy as np
from collections import Counter
import heapq
from collections.abc import Iterable


def check_feasibility(prob_info, solution):
    """
    Check if the given solution is feasible for the problem described by `prob_info`.
    This function validates the feasibility of a solution by checking the following:
    - The solution contains valid routes for all ports.
    - Routes adhere to constraints such as node indices, edge validity, and being simple.
    - Loading, unloading, and rehandling operations are performed correctly.
    - Demand requirements are satisfied at each port.
    Parameters:
    -----------
    prob_info : dict
        A dictionary containing problem information with the following keys: (there may be more keys that are not used)
        - 'N' (int): Number of nodes. (including the gate node)
        - 'E' (list of tuples): List of valid undirected edges in the graph.
        - 'K' (list of tuples): List of demands, where each demand is represented as ((origin, destination), quantity).
        - 'P' (int): Number of ports.
        - 'F' (int): Fixed cost for each route.
        - 'LB' (float): Lower bound for the objective value.
    solution : dict
        A dictionary where keys are port indices (0 to P-1) and values are lists of routes.
        Each route is represented as a tuple (route, demand_index), where:
        - `route` is a list of node indices.
        - `demand_index` is the index of the demand being handled.
    Returns
    -------
    dict
        A dictionary containing the following keys:
        - 'feasible' (bool): True if the solution is feasible, False otherwise.
        - 'obj' (float, optional): The total objective value of the solution (only if feasible).
        - 'infeasibility' (list, optional): A list of strings describing reasons for infeasibility (only if not feasible).
        - 'solution' (dict): The input solution.
    Notes:
    ------
    - A route is considered valid if it satisfies the following:
      - It has at least two nodes.
      - All nodes in the route are within valid indices.
      - The route is simple (no repeated nodes).
      - All edges in the route exist in the graph.
    - Demand-node allocations are tracked to ensure no conflicts during loading, unloading, or rehandling.
    - The function checks that all demands are correctly loaded/unloaded at the appropriate ports.    
    """




    N = prob_info['N']
    E = prob_info['E']
    E = set([(u,v) for (u,v) in E])
    K = prob_info['K']
    P = prob_info['P']
    F = prob_info['F']
    LB = prob_info['LB']

    # Current status of nodes
    # -1 means available (i.e. empty)
    # otherwise means occupied with a demand
    node_allocations = np.ones(N, dtype=int) * -1


    # All demands that should be in the cargo at leaving port p
    supposedly_loaded_demands_after_ports = {}

    for p in range(P):
        supposedly_loaded_demands_after_ports[p] = {}
        for k,((o,d),r) in enumerate(K):
            if o <= p < d:
                supposedly_loaded_demands_after_ports[p][k] = r

    obj = 0
    infeasibility = []



    # Check solution if it has a valid structure
    if not isinstance(solution, dict):
        infeasibility.append("solution should be a dict!")

    for key, value in solution.items():
        if not isinstance(value, Iterable):
            infeasibility.append(f"Port {key} does not have a list!")

        for i, item in enumerate(value):
            if not (isinstance(item, Iterable) and len(item) == 2):
                infeasibility.append(f"{i} th value ({item}) for port {key} should be a list of (route, k)!")

            route, k = item

            if not isinstance(route, Iterable):
                infeasibility.append(f"{i} th route ({route}) for port {key} must be a list!")



    if len(infeasibility) == 0:

        for p in range(P):
            if p not in solution:
                infeasibility.append(f'The solution does not contain route list for port {p}')

            route_list = solution[p]

            for route, k in route_list:
                if len(route) <= 1:
                    infeasibility.append(f'The length of the route {route} is less than 2')
                
                if min(route) < 0 or max(route) >= N:
                    infeasibility.append(f'The route {route} has invalid node index')

                if not all(isinstance(i, int) for i in route):
                    infeasibility.append(f'The route {route} has non-integer node index')
                
                if len(route) != len(set(route)):
                    infeasibility.append(f'The route {route} has a duplicated node index, i.e., the route should be simple.')
                
                if route[0] == 0:
                    # Loading route
                    loading_node = route[-1]
                    if node_allocations[loading_node] != -1:
                        infeasibility.append(f'The loading node {loading_node} from route {route} is already occupied by demand {node_allocations[loading_node]}')
                    
                    for i in route[:-1]:
                        if node_allocations[i] != -1:
                            infeasibility.append(f'The loading route {route} is blocked by node {i} that is occupied by demand {node_allocations[i]}')
                        
                    for (u,v) in zip(route[:-1], route[1:]):
                        if (u,v) not in E and (v,u) not in E:
                            infeasibility.append(f'The route {route} contains an invalid edge {(u,v)}')
                        
                    node_allocations[loading_node] = k

                elif route[-1] == 0:
                    # Unloading route
                    unloading_node = route[0]
                    if node_allocations[unloading_node] == -1:
                        infeasibility.append(f'The unloading node {unloading_node} from route {route} is not occupied by any demand')
                    
                    for i in route[1:]:
                        if node_allocations[i] != -1:
                            infeasibility.append(f'The unloading route {route} is blocked by node {i} that is occupied by demand {node_allocations[i]}')

                    for (u,v) in zip(route[:-1], route[1:]):
                        if (u,v) not in E and (v,u) not in E:
                            infeasibility.append(f'The route {route} contains an invalid edge {(u,v)}')
                        
                    node_allocations[unloading_node] = -1

                elif route[0] != 0 and route[-1] != 0:
                    # Rehandling route
                    unloading_node = route[0]
                    loading_node = route[-1]

                    if node_allocations[unloading_node] == -1:
                        infeasibility.append(f'The unloading node {unloading_node} from route {route} is not occupied by any demand')
                    if node_allocations[loading_node] != -1:
                        infeasibility.append(f'The loading node {loading_node} from route {route} is already occupied by demand {node_allocations[loading_node]}')
                    
                    for i in route[1:-1]:
                        if node_allocations[i] != -1:
                            infeasibility.append(f'The rehandling route {route} is blocked by node {i} that is occupied by demand {node_allocations[i]}')

                    for (u,v) in zip(route[:-1], route[1:]):
                        if (u,v) not in E and (v,u) not in E:
                            infeasibility.append(f'The route {route} contains an invalid edge {(u,v)}')
                        
                    node_allocations[loading_node] = k
                    node_allocations[unloading_node] = -1


                obj += F + len(route) - 1

            
            # Check if all loading/unloading are done
            current_loading_status = Counter(node_allocations[node_allocations>=0])


            if current_loading_status != supposedly_loaded_demands_after_ports[p]:
                print(f"Current loading status: {current_loading_status}")
                print(f"Supposedly_loaded_demands_after_ports: {supposedly_loaded_demands_after_ports[p]}, {p=}")
                # This means that the loading/unloading is not done correctly
                for k,r in supposedly_loaded_demands_after_ports[p].items():
                    if k not in current_loading_status:
                        infeasibility.append(f"Demand {k} is not loaded at port {p} or before")
                    if k in current_loading_status and current_loading_status[k] != r:
                        infeasibility.append(f"Demand {k} is loaded at port {p} or before but it should be {r}, {node_allocations}")

                for k,r in current_loading_status.items():
                    if k not in supposedly_loaded_demands_after_ports[p] :
                        infeasibility.append(f"Demand {k} is loaded at port {p} or before but it should not be, {node_allocations}")



    if len(infeasibility) == 0: # All checks are passed!
        # We reduce the objective value by the lower bound
        # Lower bound is the sum of the minumum fixed costs for the demands + the sum of the minimum distance for each demand
        # Note: any demand quantity will incur two routws, one for loading and one for unloading
        
        obj = obj - LB

        checked_solution = {
            'obj': float(obj),
            'feasible': True,
            'infeasibility': None,
            'solution': solution
        }
    else:
        print(infeasibility)
        checked_solution = {
            'feasible': False,
            'infeasibility': infeasibility,
            'solution': solution
        }        

    return checked_solution




def bfs(G, node_allocations, root=0):
    """
    Perform a Breadth-First Search (BFS) traversal on a graph.
    This function starts from a specified root node and explores all reachable nodes
    in the graph, skipping over nodes that are already occupied (i.e., nodes where
    `node_allocations[node] != -1`). It returns a list of reachable nodes and their
    corresponding distances from the root node.
    Parameters:
        G (dict): A graph represented as an adjacency list, where keys are node IDs
                  and values are lists of neighboring node IDs.
        node_allocations (list | np.array): A list where each index represents a node, and the
                                 value indicates whether the node is occupied (-1
                                 means unoccupied, any other value means occupied 
                                 by the collesponding demand).
        root (int, optional): The starting node for the BFS traversal. Defaults to 0 (the gate node).
    Returns:
        tuple: A tuple containing two lists:
            - reachable_nodes (list): A list of nodes that are reachable from the root.
            - reachable_node_distances (list): A list of distances corresponding to
                                               each reachable node, indicating the
                                               number of edges from the root node.
    """

    current_layer = [root]
    visited = set(current_layer)


    reachable_nodes = []
    reachable_node_distances = []

    dist = 0
    while current_layer:
        next_layer = []
        for node in current_layer:
            for child in G[node]:
                if child not in visited and node_allocations[child] == -1:
                    visited.add(child)
                    next_layer.append(child)
        current_layer = next_layer
        dist += 1
        reachable_nodes.extend(current_layer)
        reachable_node_distances.extend([dist] * len(current_layer))
    
    return reachable_nodes, reachable_node_distances


def get_available_nodes(node_allocations):
    """
    Get the available nodes in the graph that are not occupied.
    """

    return [n for n,alloc in enumerate(node_allocations) if alloc == -1][1:] # # Excluding the gate node


def dijkstra(G, node_allocations=None, start=0):
    """
    Perform Dijkstra's algorithm to find the shortest path from a starting node to all other nodes in a graph.
    Parameters:
        G (dict): A dictionary representing the graph where keys are nodes and values are lists of neighboring nodes.
        node_allocations (list or None, optional): A list indicating the allocation status of nodes. If provided, nodes 
            with a value other than -1 are considered occupied and will be skipped during the algorithm. Defaults to None.
        start (int, optional): The starting node for the algorithm. Defaults to 0.
    Returns:
        tuple:
            - distances (dict): A dictionary where keys are nodes and values are the shortest distances from the start node.
            - previous_nodes (dict): A dictionary where keys are nodes and values are the previous node in the shortest path.
    Notes:
        - The graph `G` is assumed to be unweighted, and the distance between any two connected nodes is considered to be 1.
        - If `node_allocations` is provided, the algorithm will skip over nodes that are occupied (i.e., `node_allocations[node] != -1`).
    """
    
    distances = {node: float('inf') for node in G}
    distances[start] = 0

    previous_nodes = {node: None for node in G}

    priority_queue = [(0, start)]  # (distance, node)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in G[current_node]:
            if node_allocations is None or node_allocations[neighbor] == -1:
                distance = current_distance + 1

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes


def path_backtracking(previous_nodes, start, target):
    """
    Backtrack the path from the target node to the start node using the previous_nodes dictionary.
    Args:
        previous_nodes (dict): A dictionary where keys are nodes and values are the preceding node 
                               in the path for each key.
        start: The starting node of the path.
        target: The target node from which the backtracking begins.

    Returns:
        list: A list of nodes representing the path from the start node to the target node, 
              in the correct order.

    Raises:
        KeyError: If a node in the backtracking process is not found in the previous_nodes dictionary.
    """

    path = []
    current_node = target
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()  
    return path




