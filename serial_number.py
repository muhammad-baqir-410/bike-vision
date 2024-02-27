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
# Use the function and print the serial number
serial_number = get_raspberry_pi_serial_number()
if serial_number:
    print(f"Raspberry Pi Serial Number: {serial_number}")
else:
    print("Failed to read the Raspberry Pi Serial Number.")