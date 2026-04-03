def find_path(current, destination, candidate, candidates, network, visited):
    if current in network:
        if len(network[current]) >= 1:
            for i in range (len(network[current])):
                if network[current][i][0] == destination:
                    candidate.append((network[current][i][0],network[current][i][1],network[current][i][2],network[current][i][3]))
                    candidates.append([stop for stop in candidate])
                elif not(network[current][i][0] in visited):
                    temp = [stop for stop in candidate]
                    temp_visited = [stop for stop in visited]
                    visited.append(network[current][i][0])
                    candidate.append((network[current][i][0],network[current][i][3]))
                    find_path(network[current][i][0], destination, candidate, candidates, network, visited)
                    candidate = [stop for stop in temp]
                    visited = [stop for stop in temp_visited]


def get_candidates(origin,destination,network):
    candidates = []
    candidate = []
    visited = [origin]
    find_path(origin,destination,candidate,candidates,network,visited)
    return candidates

