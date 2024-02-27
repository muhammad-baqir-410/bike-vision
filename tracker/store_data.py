
from datetime import datetime
import requests
import json
import os

# Path to your JSON file
# json_file_path = 'data.json'

# Your API Gateway endpoint URL (replace with your actual URL)
api_url = 'https://q6f8jxco8g.execute-api.us-east-1.amazonaws.com/bike/storeData'


def find_unique_class_counts(data):
    result = {}
    for tracking_id, values in data.items():
        if values not in result:
            result[values] = 1
        else:
            result[values] += 1

    return result
    # print(result)



def get_raspberry_pi_serial_number():
    # Attempt to read the serial number from /proc/cpuinfo
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    # Extract the serial number
                    serial = line.strip().split(':')[1].strip()
                    return serial
    except Exception as e:
        print(f"Error reading serial number: {e}")
        return None
    

def get_device_id():
    # Check if the serial number file exists
    if os.path.exists("serial_number.txt"):
        # Read the serial number from the file
        with open("serial_number.txt", "r") as f:
            serial_number = f.read().strip()
        print(f"Raspberry Pi Serial Number read from file: {serial_number}")
        return serial_number
    else:
        # Get the serial number from the system and write it to the file
        serial_number = get_raspberry_pi_serial_number()
        if serial_number:
            with open("serial_number.txt", "w") as f:
                f.write(serial_number)
            print(f"Raspberry Pi Serial Number written to serial_number.txt: {serial_number}")
            return serial_number
        else:
            print("Failed to read the Raspberry Pi Serial Number.")
            return None

def store_data(current_time, objects_track_history, lat, lon):
    data_dict = {}
    final_data = []
    time_for_data = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    # print("Current Time: ",time_for_data )
    device_id = get_device_id()
    unique_class_count = find_unique_class_counts(objects_track_history)
    data_dict["location"] = {"lat": lat, "lng": lon}
    data_dict["description"] = "Device 20"
    data_dict["bikeID"] = f"{device_id}"
    data_dict["dateTime"] = time_for_data
    data_dict["detectionData"] = unique_class_count   
    final_data.append(data_dict)
    # Convert your data to a JSON string
    data_json = json.dumps(final_data)
    print(data_json)

    # Headers to include with the request
    headers = {
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(api_url, headers=headers, data=data_json)

    # Check the response
    if response.status_code == 200:
        print('Success:', response.text)
    else:
        print('Failed:', response.status_code, response.text)

