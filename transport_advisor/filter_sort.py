def filter_sort_group(candidates: list, filter_transports: list, first_preference: int, second_preference: int) -> list:
    """
    Pass the arguments to the functions filter_mode(), rank() and group_segment() to filter, sort and group the candidates.

    Args:
        candidates (list): The list storing all the candidate.
        filter_transports (list): The list storing the transport that needs to be filtered.
        first_preference (int): The int representing the first preference.
        second_preference (int): The int representing the second preference.

    Returns:
        list: The list store candidates that is filterd, sorted and grouped according to the filter and preferences.
    """   
    filtered_candidates = filter_mode(candidates,filter_transports)
    sorted_candidates = rank(filtered_candidates, first_preference, second_preference)
    return group_segment(sorted_candidates)


def filter_mode(candidates: list, filter_transports: list) -> list:
    """
    Filter the candidates to exclude the candidate with transport in the list filter_transports.

    Args:
        candidates (list): The list storing all the candidate.
        filter_transports (list): The list storing the transport that needs to be filtered.

    Returns:
        list: The list store candidates which doesn not contain the transport that needs to be filtered.
    """   
    if len(filter_transports) == 0:
       return candidates
    filtered_candidates = []
    for candidate in candidates:
        transport_of_candidate = get_transport_mode(candidate)
        exists = False
        for transport in filter_transports:
           if transport in transport_of_candidate:
               exists = True
               break
        if not exists:
            filtered_candidates.append(candidate)
    return filtered_candidates


def rank(candidates: list, first_preference: int, second_preference: int) -> list:    # 1:time, 2:cost, 3:transfers, 4: no preference
    """
    Sort the candidates according to the preferences.

    Args:
        candidates (list): The list storing all the candidate.
        first_preference (int): The int representing the first preference.
        second_preference (int): The int representing the second preference.

    Returns:
        list: The list with the top 3 candidate sorted according to the preferences
    """
    if second_preference == 4:
        if first_preference == 1:
            second_preference = 2
        else:
            second_preference = 1
    sorted_candidates = []
    for candidate in candidates:
        time, fare = 0, 0
        number_of_transfer = count_transfer(get_transport_mode(candidate))
        for segment in candidate:
            time += segment[1]
            fare += segment[2]
        sorted_candidates.append([candidate,time,fare, number_of_transfer])
    third_preference = list({1,2,3}-{first_preference,second_preference})[0]   # Use set difference to dynamically determine the tie-breaker preference
    sorted_candidates = sorted(sorted_candidates, key = lambda x: (x[first_preference], x[second_preference], x[third_preference]))   # Sort journeys sequentially by 1st, 2nd, and 3rd preferences using a tuple key
    if len(sorted_candidates) > 3:
        return [sorted_candidates[i] for i in range(3)]
    else:
        return sorted_candidates


def group_segment(candidates: list) -> list:
    """
    Group the segments of the candidates by transport mode.

    Args:
        candidates (list): The list storing all the candidate.

    Returns:
        list: The list storing each candidate in which neighboring segments are grouped by transport mode.
    """
    final_candidates = []
    for candidate in candidates:
        segment = 0
        grouped_candidate =[]
        if len(candidate[0]) == 1:
            grouped_candidate.append([[candidate[0][segment][0]], candidate[0][segment][3], candidate[0][segment][1]])
        while segment < len(candidate[0])-1:
            stop_list = [candidate[0][segment][0]]
            duration = candidate[0][segment][1]
            transport = candidate[0][segment][3]

            # Inner loop: If the next segment uses the exact same transport mode, 
            # merge them by accumulating the total duration and appending the next stop.
            while (segment < len(candidate[0])-1) and (candidate[0][segment][3] == candidate[0][segment+1][3]):
                segment += 1
                stop_list.append(candidate[0][segment][0])
                duration += candidate[0][segment][1]

            # Save the fully grouped leg of the journey
            grouped_candidate.append([stop_list, transport, duration])
            segment += 1

            # Edge case: Check if the very last segment of the journey is a different transport mode from the group that is just processed
            if (segment == len(candidate[0])-1) and (candidate[0][segment-1][3] != candidate[0][segment][3]):
                grouped_candidate.append([[candidate[0][segment][0]], candidate[0][segment][3], candidate[0][segment][1]])
        final_candidates.append([grouped_candidate, candidate[1], candidate[2], candidate[3]])
    return final_candidates


def count_transfer(transport_mode: list) -> int:
    """
    Get the number of transfer for the given list with transport_modes of a path.

    Args:
        transport_mode (list): The list storing the transport_mode of a path.

    Returns:
        int: Number of transfer.
    """
    if len(transport_mode) == 1:
        return 0
    count = 0
    while ('Walking' in transport_mode):
        pos = transport_mode.index('Walking')
        if pos == 0 or pos == len(transport_mode) - 1:         # Walking at the very beginning or very end of a journey doesn't count as a transfer
            transport_mode.pop(pos)
        else:
            if transport_mode[pos-1] == transport_mode[pos+1]: # If walking bridges the exact same transport (e.g., Bus -> Walk -> Bus),
                count += 1                                     # it counts as 1 transfer. Otherwise, it bridges different modes.
            transport_mode.pop(pos)
    for i in range(len(transport_mode)-1):
        if transport_mode[i] != transport_mode[i+1]:           # Count transfers for all remaining transport changes
            count += 1
    return count


def get_transport_mode(candidate: list) -> list:
    """
    Get the transport modes of the given candidate.

    Args:
        candidate (list): The list storing the path of the journey.

    Returns:
        list: Stores the transport modes of the given candidate (in the same order of the path).
    """
    transport_of_candidate = []
    for segment in candidate:
        transport_of_candidate.append(segment[3])
    return transport_of_candidate
