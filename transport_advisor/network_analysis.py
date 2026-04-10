def SummarizeNetwork(network):
    n_stops = len(network)
    n_segments, n_bsegments, n_wsegments, n_msegments = 0, 0, 0, 0
    for segment_list in network.values():
        for segment in segment_list:
            if segment[3] == "Bus":
                n_bsegments += 1
            elif segment[3] == "Walking":
                n_wsegments += 1
            else:
                n_msegments += 1
            n_segments += 1
    
    return n_stops, n_segments, n_bsegments, n_wsegments, n_msegments

def get_distinct_transport(network):
    transport_mode_distinct = []
    for stop in network:
        for segment in network[stop]:
          transport_mode_distinct.append(segment[3])
    return list(set(transport_mode_distinct))
