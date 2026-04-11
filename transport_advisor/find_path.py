def find_path(current, destination, candidate, candidates, network, visited):
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
                    

def get_candidates(origin,destination,network):
    candidates = []
    candidate = [] 
    visited = [origin]
    find_path(origin,destination,candidate,candidates,network,visited)
    return candidates
