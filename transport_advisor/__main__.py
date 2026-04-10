try:
    import transport_advisor.find_path as find_path
    import transport_advisor.filter_sort as filter_sort
    import transport_advisor.network_analysis as network_analysis
    import transport_advisor.load_network as load_network
except ImportError:
    print("\033[33mPlease run the following from the root directory:\x1b[0m python -m transport_advisor")
    exit()

try:
    from readchar import readkey
except ImportError:
    print("\x1b[31mMissing dependency detected!\x1b[0m Please run: pip install -r requirements.txt")
    exit()

def OnStart():
    banner = """                                                                                                                                                                               
 ▄▄▄▄▄▄▄                              ▄▄▄▄▄▄▄         ▄▄    ▄▄             ▄▄▄▄▄▄▄▄▄                                                  ▄▄▄▄      ▄▄                             
█████▀▀▀                       ██     ███▀▀███▄       ██    ██ ▀▀          ▀▀▀███▀▀▀                                         ██     ▄██▀▀██▄    ██       ▀▀                    
 ▀████▄  ███▄███▄  ▀▀█▄ ████▄ ▀██▀▀   ███▄▄███▀ ██ ██ ████▄ ██ ██  ▄████      ███ ████▄  ▀▀█▄ ████▄ ▄█▀▀▀ ████▄ ▄███▄ ████▄ ▀██▀▀   ███  ███ ▄████ ██ ██ ██  ▄█▀▀▀ ▄███▄ ████▄ 
   ▀████ ██ ██ ██ ▄█▀██ ██ ▀▀  ██     ███▀▀▀▀   ██ ██ ██ ██ ██ ██  ██         ███ ██ ▀▀ ▄█▀██ ██ ██ ▀███▄ ██ ██ ██ ██ ██ ▀▀  ██     ███▀▀███ ██ ██ ██▄██ ██  ▀███▄ ██ ██ ██ ▀▀ 
███████▀ ██ ██ ██ ▀█▄██ ██     ██     ███       ▀██▀█ ████▀ ██ ██▄ ▀████      ███ ██    ▀█▄██ ██ ██ ▄▄▄█▀ ████▀ ▀███▀ ██     ██     ███  ███ ▀████  ▀█▀  ██▄ ▄▄▄█▀ ▀███▀ ██    
                                                                                                          ██                                                                   
                                                                                                          ▀▀                                                                   """
    print(banner+"\nThanks for using Smart Public Transport Advisor!\n<Please read the README.md for detailed user guide>\n")

def ClearLines(n):
    print("\033[F\033[K"*n, flush=True, end="")

def main():
    OnStart()
    print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
    network = dict()
    command = readkey()
    while command != "4":
        if command == "1" and len(network) != 0:
            ClearLines(5)
            origin = input("Enter origin: ")
            while not(origin in network):
                ClearLines(1)
                origin = input("\x1b[31mStop not found!\x1b[0m\nEnter origin again: ")
            print("")

            destination = input("Enter destination: ")
            while not(destination in network) or destination == origin:
                ClearLines(1)
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
                    ClearLines(3)
                    print("Choose first preference:\n1: Fastest Journeys\n2: Cheapest Journeys\n3: Journeys with Fewest Transfers")
                    preference1 = readkey()
                    while not preference1 in ("1", "2", "3"):
                        preference1 = readkey()
                    preference1 = int(preference1)
                    
                    secondprompt = ("\n1: Cheapest Journeys\n2: Journeys with Fewest Transfers", "\n1: Fastest Journeys\n2: Journeys with Fewest Transfers", "\n1: Fastest Journeys\n2: Cheapest Journeys")[preference1-1]
                    print("\nChoose second preference:"+secondprompt+"\n3: No Preference")
                    preference2 = readkey()
                    while not preference2 in ("1", "2", "3"):
                        preference2 = readkey()
                    if preference1 == 1 or (preference1 == 2 and preference2 == "2") or preference2 == "3": #accomodate for decrement of command numbers
                        preference2 = int(preference2) + 1
                    preference2 = int(preference2)
                    
                    transports = network_analysis.get_distinct_transport(network)
                    print("\nChoose transport filter (if any):", end="")
                    for i, transport in enumerate(transports):
                        print(f"\n{i+1}: {transport}", end="")
                    print(f"\n{len(transports)+1}: No Filter")
                    transport_filter = readkey()
                    while not transport_filter in (str(i+1) for i in range (len(transports)+1)):
                        transport_filter = readkey()
                    transport_filter = int(transport_filter)
                    
                    print("\nProcessing top journeys...")
                    processed_journeys = filter_sort.filter_sort(journeys, transport_filter, preference1, preference2, transports)
                    if len(processed_journeys) == 0:
                        print("\x1b[31mNo possible journeys found!\033[0m")
                    else:
                        print("\033[32mProcessing finished!\033[0m\n")
                        if preference2 == 4:
                            print("Top 3 journeys ranked by\033[33m", ("Fastest", "Cheapest", "Least Transfers")[preference1-1], "\x1b[0mwith\033[33m", ("No Bus", "No Metro", "No Walking", "Any Transport")[transport_filter-1]+"\x1b[0m:")
                        else:
                            print("Top 3 journeys ranked by\033[33m", ("Fastest", "Cheapest", "Least Transfers")[preference1-1], "then", ("Fastest", "Cheapest", "Least Transfers")[preference2-1], "\x1b[0mwith\033[33m", ("No Bus", "No Metro", "No Walking", "Any Transport")[transport_filter-1]+"\x1b[0m:")
                        for i in range(0, 3):
                            if len(processed_journeys) > i:
                                print(f"{origin} ", end="")
                                for segment in processed_journeys[i][0]:
                                    print(f"<{segment[1]}>--> {segment[0]} ", end="")
                                print(f"\nTotal duration: {processed_journeys[i][1]:<6}Total cost: {processed_journeys[i][2]:<10}Total transfers: {processed_journeys[i][3]:<5}\n")
                        
                    print("\nAwaiting next command...\n1: View Top Journeys\n2: Return to Start")

                command = readkey()

            print("\nAvailable commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")

        elif command == "2":
            ClearLines(5)
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

        elif command == "3":
            ClearLines(5)
            n_stops, n_segments, n_bsegments, n_wsegments, n_msegments = network_analysis.SummarizeNetwork(network)
            print("Stops: ", end="")
            for stop in network:
                print(stop+", ", end="")
            print(f"\b\b  \nTotal Stops: {n_stops:<10}Total Segments: {n_segments}\nBus Segments: {n_bsegments:<9}Metro Segments: {n_msegments:<7}Walking Segments: {n_wsegments}\n")
            
            if len(network) == 0:
                print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
            else:
                print("Available commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")

        command = readkey()

    print("\nQuitting...")
    exit()

if __name__ == "__main__":
    main()
