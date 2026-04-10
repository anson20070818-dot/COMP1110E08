def filter_mode(candidates, filter, transports):    
    if filter == len(transports)+1:
       return candidates
    filtered_candidates = []
    for candidate in candidates:
        transport_mode = get_transport_mode(candidate)
        if transports[filter-1] not in transport_mode:
            filtered_candidates.append(candidate)
    return filtered_candidates


def rank(candidates, first_preference, second_preference):    # 1:time, 2:cost, 3:transfers, 4: no preference
    if second_preference == 4:
        if first_preference == 1:
            second_preference = 2
        else:
            second_preference = 1
    final_candidates = []
    for candidate in candidates:
        route = []
        time, fare = 0, 0
        number_of_transfer = count_transfer(get_transport_mode(candidate))
        for segment in candidate:
            time += segment[1]
            fare += segment[2]
            route.append((segment[0],segment[3]))
        final_candidates.append([route,time,fare, number_of_transfer])
    third_preference = list({1,2,3}-{first_preference,second_preference})[0]
    return sorted(final_candidates, key = lambda x: (x[first_preference], x[second_preference], x[third_preference]))
    

def filter_sort(candidates, filter, first_preference, second_preference, transports):
    return rank(filter_mode(candidates,filter, transports), first_preference, second_preference)


def count_transfer(transport_mode):
    if len(transport_mode) == 1:
        return 0
    count = 0
    if transport_mode[0] == 'Walking' and (('Bus' in transport_mode) or ('MTR' in transport_mode)):
        count += 1
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
    transport_mode = []
    for i in range(len(candidate)):
        transport_mode.append(candidate[i][3])
    return transport_mode

