def find_path(current: str, destination: str, candidate: list, candidates: list, network: dict, visited: list) -> None:
    """
    Apply depth search using recursive logic to find all possible ways to travel from origin to destination. 
    Append all the candidate to a list.

    Args:
        current (string): The current stop of the path.
        destination (string): The destination of the journey.
        candidate (list): The list with stop information of a path.
        candidates (list): The list with all candidate.
        network (dict): A network with stops as key, a list of segments as value
        visited (list): The list with all visited stops.

    Returns:
        None
        
    """
    if current in network:                                                   # Verify the current stop has outbound connections
        for to_stop in network[current]:                                     # Iterate through all available transport segments from this stop
            if to_stop[0] == destination:                                    # Check if the segment destination matches our target
                candidate.append(tuple(to_stop))                             # Add the final reaching segment to the current path
                candidates.append(list(candidate))                           # Store a deep copy of the completed journey in the candidates list
                candidate.pop()                                              # Backtrack: remove the target stop to explore other paths to the same target
            elif to_stop[0] not in visited:                                  # Prevent infinite loops by checking if stop was already visited
                visited.append(to_stop[0])                                   # Mark the new stop as visited for this specific branch
                candidate.append(tuple(to_stop))                             # Add the intermediate segment to the growing path
                find_path(to_stop[0], destination, candidate, candidates, network, visited)   # Recursively explore deeper from the new stop
                candidate.pop()                                              # Backtrack: remove the last segment to try different routes from previous stop
                visited.pop()                                                # Unmark the stop so it can be used in other independent branches
                    

def get_candidates(origin: str,destination: str,network: dict) -> list:
    """
    Get the candidates (path for journey) for the given origin, destination and network.

    Args:
        origin (string): The origin of the journey.
        destination (string): The destination of the journey.
        network (dict): A network with stops as key, a list of segments as value

    Returns:
        list: Stores all possible candidate for the given args.
        
    """
    candidates = []                                                          # Initialize empty list to collect all valid journey paths
    candidate = []                                                           # Initialize list to track the path of the current recursive branch
    visited = [origin]                                                       # Initialize visited list with the starting point to avoid immediate cycles
    find_path(origin,destination,candidate,candidates,network,visited)       # Execute the recursive path-finding search
    return candidates                                                        # Return the full collection of discovered journeys
