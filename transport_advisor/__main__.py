# Ensure program is executed as a module
try:
    import transport_advisor.find_path as find_path
    import transport_advisor.filter_sort as filter_sort
    import transport_advisor.network_analysis as network_analysis
    import transport_advisor.load_network as load_network
except ImportError:
    print("\033[33mPlease run the following from the root directory:\x1b[0m python -m transport_advisor")
    exit()

# Ensure dependencies are installed
try:
    from readchar import readkey
except ImportError:
    print("\x1b[31mMissing dependency detected!\x1b[0m Please run: pip install -r requirements.txt")
    exit()

def on_start() -> None:
    """
    Prints title screen and greeting

    Args:
        None
    
    Returns:
        None
    """
    banner = """                                                                                                                                                                               
 ▄▄▄▄▄▄▄                              ▄▄▄▄▄▄▄         ▄▄    ▄▄             ▄▄▄▄▄▄▄▄▄                                                  ▄▄▄▄      ▄▄                             
█████▀▀▀                       ██     ███▀▀███▄       ██    ██ ▀▀          ▀▀▀███▀▀▀                                         ██     ▄██▀▀██▄    ██       ▀▀                    
 ▀████▄  ███▄███▄  ▀▀█▄ ████▄ ▀██▀▀   ███▄▄███▀ ██ ██ ████▄ ██ ██  ▄████      ███ ████▄  ▀▀█▄ ████▄ ▄█▀▀▀ ████▄ ▄███▄ ████▄ ▀██▀▀   ███  ███ ▄████ ██ ██ ██  ▄█▀▀▀ ▄███▄ ████▄ 
   ▀████ ██ ██ ██ ▄█▀██ ██ ▀▀  ██     ███▀▀▀▀   ██ ██ ██ ██ ██ ██  ██         ███ ██ ▀▀ ▄█▀██ ██ ██ ▀███▄ ██ ██ ██ ██ ██ ▀▀  ██     ███▀▀███ ██ ██ ██▄██ ██  ▀███▄ ██ ██ ██ ▀▀ 
███████▀ ██ ██ ██ ▀█▄██ ██     ██     ███       ▀██▀█ ████▀ ██ ██▄ ▀████      ███ ██    ▀█▄██ ██ ██ ▄▄▄█▀ ████▀ ▀███▀ ██     ██     ███  ███ ▀████  ▀█▀  ██▄ ▄▄▄█▀ ▀███▀ ██    
                                                                                                          ██                                                                   
                                                                                                          ▀▀                                                                   """
    print("\x1b[34m"+banner+"\x1b[0m\nThanks for using Smart Public Transport Advisor!\n<Please refer to the README.md for detailed user guide>\n")

def clear_lines(n: int) -> None:
    """
    Remove all text from n lines counting from the bottom

    Args:
        n (int): Number of lines to clear
    
    Returns:
        None
    """
    print("\033[F\033[K"*n, flush=True, end="")

def main() -> None:
    on_start()
    print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
    network = dict()
    command = readkey()
    # Quit Program if 4
    while command != "4":
        # Generate Journeys
        if command == "1" and len(network) != 0:    # Prevent command execution when network is not loaded
            clear_lines(5)
            origin = input("Enter origin: ")
            while not(origin in network):
                clear_lines(1)
                origin = input("\x1b[31mStop not found!\x1b[0m\nEnter origin again: ")
            print("")

            destination = input("Enter destination: ")
            while not(destination in network) or destination == origin:
                clear_lines(1)
                if destination == origin:
                    destination = input("\x1b[31mDestination cannot be the same as Origin!\x1b[0m\nEnter destination again: ")
                else:
                    destination = input("\x1b[31mStop not found!\x1b[0m\nEnter destination again: ")

            print("\nGenerating journeys...")
            journeys = find_path.get_candidates(origin, destination, network)
            print("\033[32mJourneys successfully generated!\033[0m\n")
            print("Awaiting next command...\n1: View Top Journeys\n2: Return to Start")
            command = readkey()
            while command != "2":
                if command == "1":
                    clear_lines(3)
                    print("Choose first preference:\n1: Fastest Journeys\n2: Cheapest Journeys\n3: Journeys with Fewest Transfers")
                    preference1 = readkey()
                    while not preference1 in ("1", "2", "3"):
                        preference1 = readkey()
                    preference1 = int(preference1)
                    
                    # Dynamically hide the first preference from the list of second-preference choices
                    secondprompt = ("\n1: Cheapest Journeys\n2: Journeys with Fewest Transfers", "\n1: Fastest Journeys\n2: Journeys with Fewest Transfers", "\n1: Fastest Journeys\n2: Cheapest Journeys")[preference1-1]
                    print("\nChoose second preference:"+secondprompt+"\n3: No Preference")
                    preference2 = readkey()
                    while not preference2 in ("1", "2", "3"):
                        preference2 = readkey()
                    if preference1 == 1 or (preference1 == 2 and preference2 == "2") or preference2 == "3": # Correct index values of second preference
                        preference2 = int(preference2) + 1
                    preference2 = int(preference2)
                    
                    transports = network_analysis.get_distinct_transport(network)
                    print("\nChoose transport filter (if any):", end="")
                    for i, transport in enumerate(transports):
                        print(f"\n{i+1}: {transport}", end="")
                    print(f"\n{len(transports)+1}: Finish Filter Input")
                    transport_input = readkey()
                    transport_filter = list()
                    while transport_input != str(len(transports) + 1):
                        if transport_input in (str(i+1) for i in range (len(transports))):
                            transport_filter.append(transports.pop(int(transport_input) - 1)) # Remove chosen mode from available options
                            if len(transports) == 1:
                                break
                            clear_lines(len(transports) + 2)
                            for i, transport in enumerate(transports):
                                print(f"{i+1}: {transport}")
                            print(f"{len(transports)+1}: Finish Filter Input")
                        transport_input = readkey()

                    print("\nProcessing top journeys...")
                    processed_journeys = filter_sort.filter_sort_group(journeys, transport_filter, preference1, preference2)

                    if len(processed_journeys) == 0:
                        print("\x1b[31mNo possible journeys found!\033[0m")
                    else:
                        print("\033[32mProcessing finished!\033[0m\n")
                        filter_string = "Any Tranport" if len(transport_filter) == 0 else f"No {transport_filter[0]}"
                        for i in range(1, len(transport_filter)):
                            filter_string += f", {transport_filter[i]}"
                        if preference2 == 4:
                            print("Top 3 journeys ranked by\033[33m", ("Fastest", "Cheapest", "Least Transfers")[preference1-1], "\x1b[0mwith\033[33m", filter_string+"\x1b[0m:")
                        else:
                            print("Top 3 journeys ranked by\033[33m", ("Fastest", "Cheapest", "Least Transfers")[preference1-1], "then", ("Fastest", "Cheapest", "Least Transfers")[preference2-1], "\x1b[0mwith\033[33m", filter_string+"\x1b[0m:")
                        last_stop = origin
                        for journey in processed_journeys:
                            for grouped_segments in journey[0]:
                                print(f"{grouped_segments[1]}: {last_stop}", end="")
                                for stop in grouped_segments[0]:
                                    print(f" -> {stop}", end="")
                                print(f" ({grouped_segments[2]} minutes)")
                                last_stop = grouped_segments[0][-1]
                            last_stop = origin
                            print(f"Total duration: {journey[1]:<6}Total cost: {journey[2]:<10}Total transfers: {journey[3]:<5}\n")
                    
                    print("\nAwaiting next command...\n1: View Top Journeys\n2: Return to Start")

                command = readkey()

            print("\nAvailable commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")
        # Load Network
        elif command == "2":
            clear_lines(5)
            filename = input("Enter network file name (with path): ")
            print("\nLoading network file...")
            result = load_network.load_network(filename)
            if result != None:
                network = result
            print("")

            if len(network) == 0:
                print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
            else:
                print("Available commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")
        # View Network Summary
        elif command == "3":
            clear_lines(5)
            n_stops, n_segments, t_segments = network_analysis.summarize_network(network)
            print("Stops: ", end="")
            for stop in network:
                print(stop+", ", end="")
            print(f"\b\b  \nTotal Stops: {n_stops:<14}Total Segments: {n_segments}")
            for transport, segments in t_segments.items():
                print(f"{transport} Segments: {segments:<{16-len(transport)}}", end="")
            
            print("\n")
            if len(network) == 0:
                print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
            else:
                print("Available commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")

        command = readkey()

    print("\nQuitting...")
    exit()

if __name__ == "__main__":
    main()
