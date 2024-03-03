import json
import uuid
from datetime import datetime

# Replace 'file_path1' and 'file_path2' with the paths to your actual JSON files
file_path1 = 'euroleague_schedule_2024.json'
file_path2 = 'NBA_schedule_2024.json'
file_path3 = 'NHL_schedule_2024.json'

# Adjusted function to handle dates that might be integers (timestamps)
def parse_date(date):
    if isinstance(date, int):
        # Assuming the timestamp is in milliseconds, convert to seconds
        return datetime.utcfromtimestamp(date / 1000)
    elif isinstance(date, str):
        # Adjust this format to match your actual date string format if necessary
        return datetime.strptime(date, "%Y-%m-%d")
    else:
        raise ValueError("Date must be str or int")

# Read and load the JSON data from files
with open(file_path1, 'r') as file:
    data1 = json.load(file)
with open(file_path2, 'r') as file:
    data2 = json.load(file)
with open(file_path3, 'r') as file:
    data3 = json.load(file)

# Merge the data from both files
merged_data = data1 + data2 + data3

# Sort the merged data by date
merged_data.sort(key=lambda event: parse_date(event['Date']))

# Add a unique event ID to each event in the merged data
for i, event in enumerate(merged_data, start=1):
    event['EventID'] = i  # or use uuid.uuid4() for a UUID

# Write the sorted and updated merged data to a new JSON file
with open('merged_data_with_ids.json', 'w') as file:
    json.dump(merged_data, file, indent=4)
