def find_path(current: str, destination: str, candidate: list, candidates: list, network: dict, visited: list) -> None:
    """
    Apply depth search using recursive logic to find all possible ways to travel from origin to destination. 
    Append all the candidate to a list.

    Args:
        current (string): The current stop of the path.
        destination (string): The destination of the journey.
        candidate (list): The list with stop information of a path.
        candidates (list): The list with all candidate.
        network (dictionary): The information of segments of the network.
        visited (list): The list with all visited stops.

    Returns:
        None
        
    """
    if current in network:
        for to_stop in network[current]:
            if to_stop[0] == destination:
                candidate.append(tuple(to_stop))
                candidates.append(list(candidate))
                candidate.pop()
            elif to_stop[0] not in visited:
                visited.append(to_stop[0])
                candidate.append(tuple(to_stop))
                find_path(to_stop[0], destination, candidate, candidates, network, visited)
                candidate.pop()
                visited.pop()
                    

def get_candidates(origin: str,destination: str,network: dict) -> list:
    """
    Get the candidates (path for journey) for the given origin, destination and network.

    Args:
        origin (string): The origin of the journey.
        destination (string): The destination of the journey.
        network (dictionary): The information of segments of the network.

    Returns:
        list: Stores all possible candidate for the given args.
        
    """
    candidates = []
    candidate = [] 
    visited = [origin]
    find_path(origin,destination,candidate,candidates,network,visited)
    return candidates
