def SummarizeNetwork(network):
    n_stops = len(network)
    n_segments = 0
    t_segments = dict()
    for segment_list in network.values():
        for segment in segment_list:
            if t_segments.get(segment[3], -1) == -1:
                t_segments[segment[3]] = 1
            else:
                t_segments[segment[3]] += 1
            n_segments += 1
    
    return n_stops, n_segments, t_segments

def get_distinct_transport(network: dict) -> list:
    """
    Get the dictinct transport modes for the given network.

    Args:
        network (dictionary): The information of segments of the network.

    Returns:
        list: Stores all the (distinct) transport modes of a network
        
    """
    transport_mode_distinct = []
    for stop in network:
        for segment in network[stop]:
          transport_mode_distinct.append(segment[3])
    return list(set(transport_mode_distinct))
