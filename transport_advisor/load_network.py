import csv
from pathlib import Path

def load_network(filename: str = "network.csv") -> dict | None:
    """
    Fetch network data from the data folder

    Args:
        filename (string): Name of the network csv file, default network.csv

    Returns:
        Dict or None: Dictionary of processed data with stops as keys and
        segments as values if file is found and there is at least 1 good row,
        else None
    """
    if filename == "":
        filename = "network.csv"
        
    segments = dict()  

    try:
        file_dir = Path(__file__).parent.parent
        file_path = file_dir / "data" / filename
        file = open(file_path, "r", encoding="utf-8")
        reader = csv.DictReader(file)

        first_row = next(reader, None)
        if first_row is None:
            print("\x1b[31mError: The network file is empty!\x1b[0m")
            file.close()
            return None

        # Go back to the beginning and read all rows
        file.seek(0)
        reader = csv.DictReader(file)

        valid_segments = 0
        for i, row in enumerate(reader):
            try:
                segment = []
                segment_reverse = []
                if int(row['Duration']) < 0:
                    print(f"\033[33mWarning: Skipped row {i+1} in the file due to negative duration\033[0m")
                    continue
                if float(row['Cost']) < 0:
                    print(f"\033[33mWarning: Skipped row {i+1} in the file due to negative cost\033[0m")
                    continue
                for j in ['To_Stop','Duration','Cost','Mode']:
                    if j in ['To_Stop','Mode']:
                        segment.append(row[j].strip())
                    elif j == 'Duration':
                        segment.append(int(row[j]))
                    else:
                        segment.append(float(row[j]))
                if row['From_Stop'].strip() in segments:
                    if segment not in segments[row['From_Stop'].strip()]:
                        segments[row['From_Stop'].strip()].append(segment)
                else:
                    segments[row['From_Stop'].strip()] = [segment]
                for j in ['From_Stop','Duration','Cost','Mode']:
                    if j in ['From_Stop','Mode']:
                        segment_reverse.append(row[j].strip())
                    elif j == 'Duration':
                        segment_reverse.append(int(row[j]))
                    else:
                        segment_reverse.append(float(row[j]))
                if row['To_Stop'].strip() in segments:
                    if segment_reverse not in segments[row['To_Stop'].strip()]:
                        segments[row['To_Stop'].strip()].append(segment_reverse)
                else:
                    segments[row['To_Stop'].strip()] = [segment_reverse]
                valid_segments += 1
            except:
                print(f"\033[33mWarning: Skipped bad row (row {i+1}) in the file\033[0m")
                continue

        file.close()

        if len(segments) == 0:
            print("\x1b[31mError: No valid segments in the file!\x1b[0m")
            return None
        
        if valid_segments*2 > 100:
            print("\x1b[31mError: Total segments exceeded 100! Try a smaller network\x1b[0m")
            return None

        print("\033[32mSuccessfully loaded", len(segments), "stops from the file\x1b[0m")
        return segments

    except FileNotFoundError:
        print("\x1b[31mError: Cannot find the file\x1b[0m", filename)
        print("Make sure the file is inside the 'data' folder")
        return None
    except Exception as e:
        print("\x1b[31mError loading the network:\x1b[0m", str(e))
        return None
