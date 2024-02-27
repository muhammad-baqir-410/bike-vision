
from datetime import datetime
import requests
import json

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

def store_data(current_time, objects_track_history, lat, lon):
    data_dict = {}
    final_data = []
    time_for_data = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    # print("Current Time: ",time_for_data )
    unique_class_count = find_unique_class_counts(objects_track_history)
    data_dict["location"] = {"lat": lat, "lng": lon}
    data_dict["description"] = "Device 20"
    data_dict["bikeID"] = "20"
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



