def rank(candidate_journey,mode):
  sorted_candidate = []
  sorted_time = []
  sorted_cost = []
  if mode == "cost":
    sorted_dict = dict(sorted(candidate_journey.items(), key = lambda x: (x[1][2],x[1][1])))
  elif mode == "time":
    sorted_dict = dict(sorted(candidate_journey.items(), key = lambda x: (x[1][1],x[1][2])))
  else:
    return sorted_candidate, candidate_time, candidate_cost
  for i in range(len(sorted_dict):
    sorted_candidate.append(sorted_dict.values()[i][0])
    sorted_time.append(sorted_dict.values()[[i][1])
    sorted_cost.append(sorted_dict.values()[i][2])
  return sorted_candidate, candidate_time, candidate_cost
