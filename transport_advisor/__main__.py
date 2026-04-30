# Ensure program is executed as a module
try:
    import transport_advisor.find_path as find_path               # Imports pathfinding algorithm
    import transport_advisor.filter_sort as filter_sort           # Imports sorting and filtering logic
    import transport_advisor.network_analysis as network_analysis # Imports network summarization tools
    import transport_advisor.load_network as load_network         # Imports file I/O operations
except ImportError:
    print("\033[33mPlease run the following from the root directory:\x1b[0m python -m transport_advisor")
    exit() # Terminate if local modules cannot be found

# Ensure dependencies are installed
try:
    from readchar import readkey # Imports function to read single keystrokes without hitting Enter
except ImportError:
    print("\x1b[31mMissing dependency detected!\x1b[0m Please run: pip install -r requirements.txt")
    exit() # Terminate if third-party libraries are missing

def on_start() -> None:
    """
    Prints title screen and greeting

    Args:
        None
    
    Returns:
        None
    """
    # ASCII art banner for the application
    banner = """                                                                                                                                                                               
 ▄▄▄▄▄▄▄                              ▄▄▄▄▄▄▄         ▄▄    ▄▄             ▄▄▄▄▄▄▄▄▄                                                  ▄▄▄▄      ▄▄                             
█████▀▀▀                       ██     ███▀▀███▄       ██    ██ ▀▀          ▀▀▀███▀▀▀                                         ██     ▄██▀▀██▄    ██       ▀▀                    
 ▀████▄  ███▄███▄  ▀▀█▄ ████▄ ▀██▀▀   ███▄▄███▀ ██ ██ ████▄ ██ ██  ▄████      ███ ████▄  ▀▀█▄ ████▄ ▄█▀▀▀ ████▄ ▄███▄ ████▄ ▀██▀▀   ███  ███ ▄████ ██ ██ ██  ▄█▀▀▀ ▄███▄ ████▄ 
   ▀████ ██ ██ ██ ▄█▀██ ██ ▀▀  ██     ███▀▀▀▀   ██ ██ ██ ██ ██ ██  ██         ███ ██ ▀▀ ▄█▀██ ██ ██ ▀███▄ ██ ██ ██ ██ ██ ▀▀  ██     ███▀▀███ ██ ██ ██▄██ ██  ▀███▄ ██ ██ ██ ▀▀ 
███████▀ ██ ██ ██ ▀█▄██ ██     ██     ███       ▀██▀█ ████▀ ██ ██▄ ▀████      ███ ██    ▀█▄██ ██ ██ ▄▄▄█▀ ████▀ ▀███▀ ██     ██     ███  ███ ▀████  ▀█▀  ██▄ ▄▄▄█▀ ▀███▀ ██    
                                                                                                          ██                                                                   
                                                                                                          ▀▀                                                                   """
    # Print banner in blue (\x1b[34m) and reset color (\x1b[0m) afterwards
    print("\x1b[34m"+banner+"\x1b[0m\nThanks for using Smart Public Transport Advisor!\n<Please refer to the README.md for detailed user guide>\n")

def clear_lines(n: int) -> None:
    """
    Remove all text from n lines counting from the bottom

    Args:
        n (int): Number of lines to clear
    
    Returns:
        None
    """
    # \033[F moves the cursor up one line, \033[K clears the contents of that line
    print("\033[F\033[K"*n, flush=True, end="") 

def main() -> None:
    on_start() # Display the welcome banner
    # Print main menu options, rendering option 1 in red to indicate it is initially unavailable
    print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
    
    network = dict()         # Central storage dictionary for the loaded transport network
    command = readkey()      # Capture user's menu selection

    # Quit Program if 4
    while command != "4":    # Main application loop
        # Generate Journeys
        if command == "1" and len(network) != 0:    # Prevent command execution when network is not loaded
            clear_lines(5)                          # Clear the main menu to prepare for journey generation
            origin = input("Enter origin: ")        # Prompt for starting location
            while not(origin in network):           # Validation loop: Check if origin exists in network keys
                clear_lines(1)                      # Clear the invalid input line
                origin = input("\x1b[31mStop not found!\x1b[0m\nEnter origin again: ") # Prompt again in red
            print("")                               # Blank line for visual spacing

            destination = input("Enter destination: ") # Prompt for ending location
            while not(destination in network) or destination == origin: # Validate existence and ensure it isn't the origin
                clear_lines(1)                                          # Clear the invalid input line
                if destination == origin:
                    destination = input("\x1b[31mDestination cannot be the same as Origin!\x1b[0m\nEnter destination again: ")
                else:
                    destination = input("\x1b[31mStop not found!\x1b[0m\nEnter destination again: ")

            print("\nGenerating journeys...")
            journeys = find_path.get_candidates(origin, destination, network) # Call backend pathfinding algorithm
            print("\033[32mJourneys successfully generated!\033[0m\n")        # Print success in green
            print("Awaiting next command...\n1: View Top Journeys\n2: Return to Start")
            
            command = readkey() # Capture sub-menu selection
            while command != "2": # Sub-menu loop (Option 2 breaks out to main menu)
                if command == "1":
                    clear_lines(3) # Clear sub-menu prompt
                    print("Choose first preference:\n1: Fastest Journeys\n2: Cheapest Journeys\n3: Journeys with Fewest Transfers")
                    preference1 = readkey()                     # Capture primary sorting preference
                    while not preference1 in ("1", "2", "3"):   # Validate input is 1, 2, or 3
                        preference1 = readkey()
                    preference1 = int(preference1)              # Convert valid string to integer
                    
                    # Dynamically hide the first preference from the list of second-preference choices using tuple indexing
                    secondprompt = ("\n1: Cheapest Journeys\n2: Journeys with Fewest Transfers", "\n1: Fastest Journeys\n2: Journeys with Fewest Transfers", "\n1: Fastest Journeys\n2: Cheapest Journeys")[preference1-1]
                    print("\nChoose second preference:"+secondprompt+"\n3: No Preference")
                    preference2 = readkey()                     # Capture secondary sorting preference
                    while not preference2 in ("1", "2", "3"):   # Validate input is 1, 2, or 3
                        preference2 = readkey()
                        
                    # Correct index values of second preference to align with internal enum/constants
                    if preference1 == 1 or (preference1 == 2 and preference2 == "2") or preference2 == "3": 
                        preference2 = int(preference2) + 1      # Shift index to account for the missing primary option
                    preference2 = int(preference2)              # Convert to integer for backend processing
                    
                    transports = network_analysis.get_distinct_transport(network) # Get list of available modes
                    print("\nChoose transport filter (if any):", end="")
                    for i, transport in enumerate(transports):
                        print(f"\n{i+1}: {transport}", end="")                    # Dynamically generate list of modes to exclude
                    print(f"\n{len(transports)+1}: Finish Filter Input")
                    
                    transport_input = readkey() # Capture filter selection
                    transport_filter = list()   # Initialize list of excluded transport modes
                    
                    while transport_input != str(len(transports) + 1): # Loop until user selects "Finish" option
                        if transport_input in (str(i+1) for i in range (len(transports))):
                            transport_filter.append(transports.pop(int(transport_input) - 1)) # Remove chosen mode from available options
                            if len(transports) == 1: # If only one transport remains, stop filtering to prevent empty results
                                break
                            clear_lines(len(transports) + 2) # Clear previous filter list
                            for i, transport in enumerate(transports):
                                print(f"{i+1}: {transport}") # Reprint updated filter list
                            print(f"{len(transports)+1}: Finish Filter Input")
                        transport_input = readkey() # Capture next filter selection

                    print("\nProcessing top journeys...")
                    processed_journeys = filter_sort.filter_sort_group(journeys, transport_filter, preference1, preference2) # Rank journeys

                    if len(processed_journeys) == 0:
                        print("\x1b[31mNo possible journeys found!\033[0m") # Alert user in red if filters eliminate all routes
                    else:
                        print("\033[32mProcessing finished!\033[0m\n")      # Alert user in green upon success
                        
                        # Construct a readable string detailing the active transport exclusions
                        filter_string = "Any Transport" if len(transport_filter) == 0 else f"No {transport_filter[0]}"
                        for i in range(1, len(transport_filter)):
                            filter_string += f", {transport_filter[i]}"
                            
                        # Print header detailing the ranking criteria used
                        if preference2 == 4: # Code 4 implies "No secondary preference"
                            print("Top 3 journeys ranked by\033[33m", ("Fastest", "Cheapest", "Least Transfers")[preference1-1], "\x1b[0mwith\033[33m", filter_string+"\x1b[0m:")
                        else:
                            print("Top 3 journeys ranked by\033[33m", ("Fastest", "Cheapest", "Least Transfers")[preference1-1], "then", ("Fastest", "Cheapest", "Least Transfers")[preference2-1], "\x1b[0mwith\033[33m", filter_string+"\x1b[0m:")
                        
                        last_stop = origin # Initialize tracking variable for formatting the output path
                        for journey in processed_journeys:
                            for grouped_segments in journey[0]:
                                print(f"{grouped_segments[1]}: {last_stop}", end="") # Print the mode of transport and start stop
                                for stop in grouped_segments[0]:
                                    print(f" -> {stop}", end="")                     # Print subsequent stops in this leg
                                print(f" ({grouped_segments[2]} minutes)")           # Print duration of this specific leg
                                last_stop = grouped_segments[0][-1]                  # Update the last stop for the next leg
                            last_stop = origin                                       # Reset last stop for the next journey option
                            # Print aggregated totals for the entire journey
                            print(f"Total duration: {journey[1]:<6}Total cost: {journey[2]:<10}Total transfers: {journey[3]:<5}\n")
                    
                    print("\nAwaiting next command...\n1: View Top Journeys\n2: Return to Start")

                command = readkey() # Listen for next sub-menu command

            # Reprint main menu after returning to start
            print("\nAvailable commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")
        
        # Load Network
        elif command == "2":
            clear_lines(5)                                     # Clear main menu
            filename = input("Enter network file name (with path): ") # Get CSV filename
            print("\nLoading network file...")
            result = load_network.load_network(filename)       # Parse CSV into dictionary format
            if result != None:
                network = result                               # Update global network dictionary if successful
            print("")

            # Reprint main menu, dynamically formatting Option 1 based on load success
            if len(network) == 0:
                print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
            else:
                print("Available commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")
        
        # View Network Summary
        elif command == "3":
            clear_lines(5)                                                                    # Clear main menu
            n_stops, n_segments, t_segments = network_analysis.summarize_network(network)     # Fetch statistics
            print("Stops: ", end="")
            for stop in network:                                                              # Iterate through all network keys
                print(stop+", ", end="")
            print(f"\b\b  \nTotal Stops: {n_stops:<14}Total Segments: {n_segments}")          # Use backspaces to remove trailing comma
            for transport, segments in t_segments.items():                                    # Print mode-specific segment counts
                print(f"{transport} Segments: {segments:<{16-len(transport)}}", end="")
            
            print("\n")
            # Reprint main menu, dynamically formatting Option 1 based on load state
            if len(network) == 0:
                print("Available commands:\n\x1b[31m1: Generate Journeys (Network requires loading first!)\x1b[0m\n2: Load Network\n3: View Network Summary\n4: Quit Program")
            else:
                print("Available commands:\n1: Generate Journeys\n2: Load Network\n3: View Network Summary\n4: Quit Program")

        command = readkey() # Capture next main menu command

    print("\nQuitting...") # Exit program gracefully
    exit()

if __name__ == "__main__":
    main()
