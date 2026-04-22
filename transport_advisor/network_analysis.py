def summarize_network(network: dict) -> tuple[int, int, dict]:
    """
    Reads network and gets total stop and segments of each transport

    Args:
        network (dict): A network with stops as key, a list of segments as value
    
    Returns:
        int: Number of stops
        int: Number of segments
        dict: Transport mode (key) & Number of segments of transport (value)
    """
    n_stops = len(network)
    n_segments = 0
    t_segments = dict()
    for segment_list in network.values():
        for segment in segment_list:
            if t_segments.get(segment[3], -1) == -1:    # segment[3] is the transport mode
                t_segments[segment[3]] = 1              # initialize in dict if not found
            else:
                t_segments[segment[3]] += 1             # increment count if found
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
          transport_mode_distinct.append(segment[3])       # segment[3] is the transport mode
    return sorted(list(set(transport_mode_distinct)))      # Remove duplicate values with set and sort to ensure order 
