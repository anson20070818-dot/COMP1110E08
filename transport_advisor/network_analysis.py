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
    n_stops = len(network)                  # Total number of unique stops corresponds to the number of dictionary keys
    n_segments = 0                          # Counter to track the total number of segments
    t_segments = dict()                     # Dictionary to map each transport mode to its segment count
    
    for segment_list in network.values():   # Iterate through all outbound segment lists in the network
        for segment in segment_list:        # Iterate through individual segments originating from a stop
            if t_segments.get(segment[3], -1) == -1:    # segment[3] represents the transport mode string (e.g., 'Bus')
                t_segments[segment[3]] = 1              # Initialize the mode in dict with a count of 1 if not found
            else:
                t_segments[segment[3]] += 1             # Increment the existing count for this mode if found
            n_segments += 1                             # Increment the total global segment counter
    
    return n_stops, n_segments, t_segments

def get_distinct_transport(network: dict) -> list:
    """
    Get the dictinct transport modes for the given network.

    Args:
        network (dictionary): The information of segments of the network.

    Returns:
        list: Stores all the (distinct) transport modes of a network
        
    """
    transport_mode_distinct = []                             # Initialize an empty list to aggregate transport modes
    
    for stop in network:                                     # Iterate through each origin stop (keys)
        for segment in network[stop]:                        # Iterate through its segments (values)
          transport_mode_distinct.append(segment[3])         # Append the transport mode (segment[3]) to the list
          
    return sorted(list(set(transport_mode_distinct)))        # Remove duplicate modes using a set, then sort alphabetically to ensure consistent UI order
