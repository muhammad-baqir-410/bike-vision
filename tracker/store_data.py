
from datetime import datetime, timezone
import requests
import json
import os
import asyncio
import aiohttp
import platform
# Your API Gateway endpoint URL (replace with your actual URL)
api_url = 'https://wqmr8jsh9c.execute-api.us-east-1.amazonaws.com/bike/storeData'


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
        


def is_internet_connected(host="8.8.8.8", timeout=1):
    """
    Checks for internet availability by pinging a reliable host.

    Args:
        host: The IP address to ping (default is Google's public DNS server)
        timeout: Timeout in seconds

    Returns:
        True if internet is connected, False otherwise.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', str(timeout), host]
    return os.system(' '.join(command)) == 0


def save_json_data(data, filename):
  """
  Saves JSON-dumped data to a file.

  Args:
      data: The data to save (any JSON-serializable object).
      filename: The name of the file to save to.
  """
  try:
    with open(filename, 'w') as f:
      json.dump(data, f, indent=4)
    print(f"Data saved successfully to {filename}")
  except Exception as e:
    print(f"Error saving data: {e}")



async def send_data_to_aws(session, data, api_url, headers):
    """Sends data to AWS asynchronously and handles the response."""
    data_json = json.dumps(data)
    async with session.post(api_url, headers=headers, data=data_json) as response:
        if response.status == 200:
            print('Success:', await response.text())
            return True
        else:
            print('Failed:', response.status, await response.text())
            return False


def load_json_from_file(filename):
    """Loads JSON data from a file."""
    with open(filename, 'r') as f:
        content = f.read().strip()
        if not content:
            print(f"File {filename} is empty.")
            return {}  # or handle it as needed
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON decode error in file {filename}: {e}")
            return {} 


async def process_stored_data(session, data_directory, api_url, headers):
    """Processes stored JSON files and sends them to AWS asynchronously."""
    for filename in os.listdir(data_directory):
        if filename.endswith('.json'):
            filepath = os.path.join(data_directory, filename)
            data = load_json_from_file(filepath)
            if data:  # Check if data is not empty
                print(f"Sending data from file: {filepath}")
                success = await send_data_to_aws(session, data, api_url, headers)
                if success:
                    os.remove(filepath)
            else:
                print(f"No data to send from file: {filepath}")
                os.remove(filepath)


async def store_data(session, current_time, objects_track_history, lat, lon):
    data_dict = {}
    final_data = []
    data_directory = 'stored_data'
    # Convert the timestamp to a datetime object in UTC
    time_for_data_utc = datetime.fromtimestamp(current_time, tz=timezone.utc)
    # Convert to a string
    formatted_time_local = time_for_data_utc.strftime('%Y-%m-%d %H:%M:%S')
    device_id = get_device_id()
    if not device_id:
        device_id = "20"
    unique_class_count = find_unique_class_counts(objects_track_history)
    data_dict["location"] = {"lat": lat, "lng": lon}
    data_dict["description"] = f"Device: {device_id}"
    data_dict["bikeID"] = f"{device_id}"
    data_dict["dateTime"] = formatted_time_local
    data_dict["detectionData"] = unique_class_count   
    final_data.append(data_dict)
    # Convert your data to a JSON string
    data_json = json.dumps(final_data)
    print(data_json)
    # Headers to include with the request
    headers = {
        'Content-Type': 'application/json'
    }
    # Example usage
    if is_internet_connected():  # Ensure this check is non-blocking or refactor if necessary
        async with aiohttp.ClientSession() as session:
            if os.listdir(data_directory):
                await process_stored_data(session, data_directory,api_url, headers)  # This function needs to be async too
            response = await session.post(api_url, headers=headers, data=data_json)
            if response.status == 200:
                print('Success:', await response.text())
            else:
                print('Failed:', response.status, await response.text())
    else:
        save_json_data(final_data, f"{data_directory}/data_{formatted_time_local}.json")  # Ensure this is non-blocking or refactor if necessary
        print("No internet connection.")
