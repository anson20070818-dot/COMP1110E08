def filter_sort_group(candidates, filter_transports, first_preference, second_preference):
    filtered_candidates = filter_mode(candidates,filter_transports)
    sorted_candidates = rank(filtered_candidates, first_preference, second_preference)
    return group_segment(sorted_candidates)


def filter_mode(candidates, filter_transports):    
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


def rank(candidates, first_preference, second_preference):    # 1:time, 2:cost, 3:transfers, 4: no preference
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
    third_preference = list({1,2,3}-{first_preference,second_preference})[0]
    sorted_candidates = sorted(sorted_candidates, key = lambda x: (x[first_preference], x[second_preference], x[third_preference]))
    if len(sorted_candidates) > 3:
        return [sorted_candidates[i] for i in range(3)]
    else:
        return sorted_candidates


def group_segment(candidates):
    final_candidates = []
    for candidate in candidates:
        segment = 0
        grouped_candidate =[]
        while segment < len(candidate[0])-1:
            stop_list = [candidate[0][segment][0]]
            duration = candidate[0][segment][1]
            transport = candidate[0][segment][3]
            while (segment < len(candidate[0])-1) and (candidate[0][segment][3] == candidate[0][segment+1][3]):
                segment += 1
                stop_list.append(candidate[0][segment][0])
                duration += candidate[0][segment][1]
            grouped_candidate.append([stop_list, transport, duration])
            segment += 1
            if (segment == len(candidate[0])-1) and (candidate[0][segment-1][3] != candidate[0][segment][3]):
                grouped_candidate.append([[candidate[0][segment][0]], candidate[0][segment][3], candidate[0][segment][1]])
        final_candidates.append([grouped_candidate, candidate[1], candidate[2], candidate[3]])
    return final_candidates


def count_transfer(transport_mode):
    if len(transport_mode) == 1:
        return 0
    count = 0
    while ('Walking' in transport_mode):
        pos = transport_mode.index('Walking')
        if pos == 0 or pos == len(transport_mode) - 1:
            transport_mode.pop(pos)
        else:
            if transport_mode[pos-1] == transport_mode[pos+1]:
                count += 1
            transport_mode.pop(pos)
    for i in range(len(transport_mode)-1):
        if transport_mode[i] != transport_mode[i+1]:
            count += 1
    return count


def get_transport_mode(candidate):
    transport_of_candidate = []
    for segment in candidate:
        transport_of_candidate.append(segment[3])
    return transport_of_candidate
