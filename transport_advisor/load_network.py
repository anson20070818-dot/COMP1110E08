import csv
from pathlib import Path
from typing import Union

def load_network(filename: str = "network.csv") -> Union[dict, None]:
    """
    Fetch network data from the data folder

    Args:
        filename (string): Name of the network csv file, default network.csv

    Returns:
        Dict or None: Dictionary of processed data with stops as keys and
        segments as values if file is found and there is at least 1 good row,
        else None
    """
    if filename == "":                                                    # Fallback to default if filename is empty
        filename = "network.csv"
        
    segments = dict()                                                     # Initialize dictionary to represent the transport graph

    try:
        # Construct path: transport_advisor/data/network.csv
        file_dir = Path(__file__).parent.parent                           # Step up two levels from this script to the project root
        file_path = file_dir / "data" / filename                          # Define relative path to the 'data' subdirectory
        file = open(file_path, "r", encoding="utf-8")                     # Open file with UTF-8 encoding for cross-platform compatibility
        reader = csv.DictReader(file)                                     # Use DictReader to access columns by header names

        first_row = next(reader, None)                                    # Peek at the first row to verify file content
        if first_row is None:
            print("\x1b[31mError: The network file is empty!\x1b[0m")     # Print error in red if CSV has no data rows
            file.close()
            return None

        # Reset pointer to the start of the file to include the first row in processing
        file.seek(0)
        reader = csv.DictReader(file)

        valid_segments = 0                                                # Counter for successfully parsed transport links
        for i, row in enumerate(reader):                                  # Process the CSV row by row
            try:
                segment = []                                              # List for the forward connection (A to B)
                segment_reverse = []                                      # List for the backward connection (B to A)
                
                if float(row['Duration']) < 0:                            # Skip logic: ignore rows with impossible travel times
                    print(f"\033[33mWarning: Skipped row {i+1} in the file due to negative duration\033[0m")
                    continue
                if float(row['Cost']) < 0:                                # Skip logic: ignore rows with impossible fare values
                    print(f"\033[33mWarning: Skipped row {i+1} in the file due to negative cost\033[0m")
                    continue
                    
                # Build the forward segment data structure [To_Stop, Duration, Cost, Mode]
                for j in ['To_Stop','Duration','Cost','Mode']:
                    if j in ['To_Stop','Mode']:
                        segment.append(row[j].strip())                    # Clean whitespace from string values
                    elif j == 'Duration':
                        segment.append(float(row[j]))                     # Parse time as float
                    else:
                        segment.append(float(row[j]))                     # Parse cost as float
                        
                if row['From_Stop'].strip() in segments:                  # Map segment to the origin stop key
                    if segment not in segments[row['From_Stop'].strip()]: # Prevent redundant entries for the same route
                        segments[row['From_Stop'].strip()].append(segment)
                else:
                    segments[row['From_Stop'].strip()] = [segment]        # Create new entry if origin stop is seen for the first time

                # Build the reverse segment to ensure the graph is undirected (A <-> B)
                for j in ['From_Stop','Duration','Cost','Mode']:
                    if j in ['From_Stop','Mode']:
                        segment_reverse.append(row[j].strip())            # Clean whitespace from reverse destination stop
                    elif j == 'Duration':
                        segment_reverse.append(float(row[j]))             # Use identical duration for the return trip
                    else:
                        segment_reverse.append(float(row[j]))             # Use identical cost for the return trip
                        
                if row['To_Stop'].strip() in segments:                    # Map return segment to the destination stop key
                    if segment_reverse not in segments[row['To_Stop'].strip()]: # Prevent redundant entries
                        segments[row['To_Stop'].strip()].append(segment_reverse)
                else:
                    segments[row['To_Stop'].strip()] = [segment_reverse]  # Create new entry for reverse origin
                    
                valid_segments += 1                                       # Increment count of processed data rows
            except:                                                       # Catch any parsing errors (e.g. non-numeric strings in numeric columns)
                print(f"\033[33mWarning: Skipped bad row (row {i+1}) in the file\033[0m")
                continue

        file.close()                                                      # Ensure file resource is released

        if len(segments) == 0:                                            # Verify that at least one stop was successfully mapped
            print("\x1b[31mError: No valid segments in the file!\x1b[0m")
            return None
        
        if valid_segments*2 > 100:                                        # Constraint: prevent memory/recursion issues with oversized networks
            print("\x1b[31mError: Total segments exceeded 100! Try a smaller network\x1b[0m")
            return None

        print("\033[32mSuccessfully loaded", len(segments), "stops from the file\x1b[0m") # Success confirmation in green
        return segments

    except FileNotFoundError:                                             # Handle missing file scenario
        print("\x1b[31mError: Cannot find the file\x1b[0m", filename)
        print("Make sure the file is inside the 'data' folder")
        return None
    except Exception as e:                                                # Catch unexpected I/O or system errors
        print("\x1b[31mError loading the network:\x1b[0m", str(e))
        return None
