def get_transport_mode(candidate):
    transport_mode = []
    for segment in range(len(candidate)):
        transport_mode.append(candidate[segment][3])
    return transport_mode
