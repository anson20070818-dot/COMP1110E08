def rank(candidates, mode):
    time, fare = 0, 0
    duration = []
    cost = []
    final_candidates = []
    for i in range(len(candidates)):
        route = []
        for j in range(len(candidates[i])):
            time += candidates[i][j][1]
            fare += candidates[i][j][2]
            route.append((candidates[i][j][0],candidates[i][j][3]))
        duration.append(time)
        cost.append(fare)
        final_candidates.append([route,duration[i],cost[i]])
    if mode == "time":
        final_candidates = sorted(final_candidates, key=lambda x: (x[1], x[2]))
        return final_candidates
    elif mode == "cost":
        final_candidates = sorted(final_candidates, key=lambda x: (x[2], x[1]))
        return final_candidates