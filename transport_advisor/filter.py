def filter_mode(candidates, filter):    # 1: Bus, 2: MTR, 3: Walking, 4: no filter
    if filter == 4:
       return candidates
    filtered_candidates = []
    mode = ['Bus','MTR','Walking']
    for candidate in candidates:
        transport_mode = get_transport_mode(candidate)
        if mode[filter-1] not in transport_mode:
            filtered_candidates.append(candidate)
    return filtered_candidates
