import csv

# This function loads the transport network from the CSV file
# It returns a list of segments (each segment is a dictionary)
def load_network(filename="data/network.csv"):
    segments = []  # empty list to store all segments

    try:
        # Open the file
        file = open(filename, "r", encoding="utf-8")
        reader = csv.DictReader(file)

        # Check if the file is empty
        first_row = next(reader, None)
        if first_row is None:
            print("Error: The network file is empty!")
            file.close()
            return None

        # Go back to the beginning and read all rows
        file.seek(0)
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Convert the numbers to int and float
                segment = {
                    "From_Stop": row["From_Stop"].strip(),
                    "To_Stop": row["To_Stop"].strip(),
                    "Duration_minutes": int(row["Duration_minutes"]),
                    "Cost_HKD": float(row["Cost_HKD"]),
                    "Mode": row["Mode"].strip()
                }
                segments.append(segment)
            except:
                print("Warning: Skipped one bad row in the file")
                continue

        file.close()

        if len(segments) == 0:
            print("Error: No valid segments in the file!")
            return None

        print("Successfully loaded", len(segments), "segments from the file")
        return segments

    except FileNotFoundError:
        print("Error: Cannot find the file", filename)
        print("Make sure the file is inside the 'data' folder")
        return None
    except Exception as e:
        print("Error loading the network:", str(e))
        return None


# ==================== Test the function ====================
# This part only runs when you double-click or run this file directly
if __name__ == "__main__":
    print("=== Testing load_network ===")
    network = load_network()

    if network is not None:
        print("\nTotal segments loaded:", len(network))
        print("First segment example:")
        print(network[0])
        print("\nLast segment example:")
        print(network[-1])