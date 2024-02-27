import os

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
    

# Check if the serial number file exists
if os.path.exists("serial_number.txt"):
    # Read the serial number from the file
    with open("serial_number.txt", "r") as f:
        serial_number = f.read().strip()
    print(f"Raspberry Pi Serial Number read from file: {serial_number}")
else:
    # Get the serial number from the system and write it to the file
    serial_number = get_raspberry_pi_serial_number()
    if serial_number:
        with open("serial_number.txt", "w") as f:
            f.write(serial_number)
        print(f"Raspberry Pi Serial Number written to serial_number.txt: {serial_number}")
        
    else:
        print("Failed to read the Raspberry Pi Serial Number.")