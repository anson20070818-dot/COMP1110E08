def get_transport_mode(candidate):
    transport_mode = []
    for i in range(len(candidate)):
        transport_mode.append(candidate[i][3])
    return transport_mode
