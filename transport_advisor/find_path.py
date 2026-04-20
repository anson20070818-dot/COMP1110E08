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
    if current in network:
        for to_stop in network[current]:
            if to_stop[0] == destination:
                # Reached destination: append the final stop and save a copy of the complete path
                candidate.append(tuple(to_stop))
                candidates.append(list(candidate))

                # Backtrack: remove the destination so the loop can explore other routes
                candidate.pop()
            elif to_stop[0] not in visited:
                # Cycle avoidance: only visit stops we haven't seen in the current path
                visited.append(to_stop[0])
                candidate.append(tuple(to_stop))

                # Recursively search from this new stop
                find_path(to_stop[0], destination, candidate, candidates, network, visited)

                # Backtrack: undo the current step to explore alternative branches from the previous stop
                candidate.pop()
                visited.pop()
                    

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
    candidates = []
    candidate = [] 
    visited = [origin]
    find_path(origin,destination,candidate,candidates,network,visited)
    return candidates
