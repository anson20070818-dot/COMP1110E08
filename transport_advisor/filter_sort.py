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
    filtered_candidates = filter_mode(candidates,filter_transports)                                 # Remove journeys with excluded transport modes
    sorted_candidates = rank(filtered_candidates, first_preference, second_preference)              # Order candidates based on preferences
    return group_segment(sorted_candidates)                                                         # Consolidate consecutive segments of the same mode


def filter_mode(candidates: list, filter_transports: list) -> list:
    """
    Filter the candidates to exclude the candidate with transport in the list filter_transports.

    Args:
        candidates (list): The list storing all the candidate.
        filter_transports (list): The list storing the transport that needs to be filtered.

    Returns:
        list: The list store candidates which doesn not contain the transport that needs to be filtered.
    """   
    if len(filter_transports) == 0:                                                                 # Skip filtering if the exclusion list is empty
       return candidates
    filtered_candidates = []                                                                        # Initialize container for valid journeys
    for candidate in candidates:                                                                    # Evaluate every candidate path
        transport_of_candidate = get_transport_mode(candidate)                                      # Identify all modes used in this path
        exists = False                                                                              # Flag to track presence of a filtered mode
        for transport in filter_transports:                                                         # Compare each leg to the exclusion criteria
           if transport in transport_of_candidate:                                                  # If any leg matches a filter, flag for exclusion
               exists = True
               break
        if not exists:                                                                              # Only add journey if no excluded modes were found
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
    if second_preference == 4:                                                                      # Provide a default second choice if user has none
        if first_preference == 1:                                                                   # Default to cost if speed is the primary focus
            second_preference = 2
        else:                                                                                       # Default to time in other scenarios
            second_preference = 1
    sorted_candidates = []                                                                          # List to hold candidates with their computed metrics
    for candidate in candidates:                                                                    # Iterate through paths to calculate statistics
        time, fare = 0, 0                                                                           # Initialize counters for journey totals
        number_of_transfer = count_transfer(get_transport_mode(candidate))                          # Determine total transfers required
        for segment in candidate:                                                                   # Aggregate cost and time across all legs
            time += segment[1]
            fare += segment[2]
        sorted_candidates.append([candidate,time,fare, number_of_transfer])                         # Pair the journey data with its calculated stats
    third_preference = list({1,2,3}-{first_preference,second_preference})[0]                        # Determine the final tie-breaker automatically
    sorted_candidates = sorted(sorted_candidates, key = lambda x: (x[first_preference], x[second_preference], x[third_preference]))   # Apply hierarchical sorting
    if len(sorted_candidates) > 3:                                                                  # Restrict output to the top three results
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
    final_candidates = []                                                                           # List for candidates with consolidated legs
    for candidate in candidates:                                                                    # Process each journey for cleaner display
        segment = 0                                                                                 # Pointer for the current segment index
        grouped_candidate =[]                                                                       # Temp storage for the grouped journey segments
        if len(candidate[0]) == 1:                                                                  # Directly handle single-segment journeys
            grouped_candidate.append([[candidate[0][segment][0]], candidate[0][segment][3], candidate[0][segment][1]])
        while segment < len(candidate[0])-1:                                                        # Scan for consecutive legs with identical modes
            stop_list = [candidate[0][segment][0]]                                                  # Start a new list of stops for the current mode
            duration = candidate[0][segment][1]                                                     # Start duration counter for this grouped leg
            transport = candidate[0][segment][3]                                                    # Identify the transport mode to match against
            while (segment < len(candidate[0])-1) and (candidate[0][segment][3] == candidate[0][segment+1][3]): # Group matching legs
                segment += 1
                stop_list.append(candidate[0][segment][0])                                          # Add the intermediate stop to the leg
                duration += candidate[0][segment][1]                                                # Sum duration into the grouped leg
            grouped_candidate.append([stop_list, transport, duration])                              # Add the consolidated leg to the journey
            segment += 1                                                                            # Advance to the next potential group
            if (segment == len(candidate[0])-1) and (candidate[0][segment-1][3] != candidate[0][segment][3]):   # Handle final unique segment
                grouped_candidate.append([[candidate[0][segment][0]], candidate[0][segment][3], candidate[0][segment][1]])
        final_candidates.append([grouped_candidate, candidate[1], candidate[2], candidate[3]])      # Store the grouped journey with metrics
    return final_candidates


def count_transfer(transport_mode: list) -> int:
    """
    Get the number of transfer for the given list with transport_modes of a path.

    Args:
        transport_mode (list): The list storing the transport_mode of a path.

    Returns:
        int: Number of transfer.
    """
    if len(transport_mode) == 1:                                                                    # No transfers possible in a single-leg trip
        return 0
    count = 0                                                                                       # Initialize the transfer counter
    while ('Walking' in transport_mode):                                                            # Special logic for walking segments
        pos = transport_mode.index('Walking')
        if pos == 0 or pos == len(transport_mode) - 1:                                              # Walking at terminal ends doesn't count as transfer
            transport_mode.pop(pos)
        else:
            if transport_mode[pos-1] == transport_mode[pos+1]:                                      # Walking between same mode (e.g. Bus->Walk->Bus) counts as 1
                count += 1
            transport_mode.pop(pos)                                                                 # Remove walking to analyze remaining changes
    for i in range(len(transport_mode)-1):                                                          # Evaluate consecutive mode changes
        if transport_mode[i] != transport_mode[i+1]:                                                # Every mode shift (e.g. Bus to MTR) is a transfer
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
    transport_of_candidate = []                                                                     # Container for extracted mode strings
    for segment in candidate:                                                                       # Iterate through segment definitions
        transport_of_candidate.append(segment[3])                                                   # Pull the mode name from the segment data
    return transport_of_candidate
