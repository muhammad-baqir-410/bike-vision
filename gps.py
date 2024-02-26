import serial
import time

def is_valid_gps_data(sentence):
    """ Check if the sentence has valid GPS data """
    fields = sentence.split(',')
    if len(fields) < 6 or fields[2] == '' or fields[4] == '':
        return False
    return True

def send_at_command(ser, command, delay=1):
    ser.write((command+'\r\n').encode())
    time.sleep(delay)
    return ser.read_all().decode()

def ddm_to_dd(degrees_minutes):
    """ Convert from degrees and decimal minutes to decimal degrees """
    d, m = divmod(float(degrees_minutes), 100)
    return d + (m / 60)

def parse_gpgga(sentence):
    fields = sentence.split(',')
    lat_ddm = fields[2]
    lon_ddm = fields[4]
    lat_dir = fields[3]
    lon_dir = fields[5]

    # Convert to decimal degrees
    lat_dd = ddm_to_dd(lat_ddm)
    lon_dd = ddm_to_dd(lon_ddm)

    # Adjust for direction
    if lat_dir == 'S':
        lat_dd = -lat_dd
    if lon_dir == 'W':
        lon_dd = -lon_dd

    return lat_dd, lon_dd


# Send initial command to /dev/ttyS0
# ser_init = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)
# response = send_at_command(ser_init, 'AT+CGPS=1')
# print("Initial command response:", response)
# ser_init.close()

# # Open serial connection for continuous GPS data reading
# ser_gps = serial.Serial('/dev/ttyUSB1', baudrate=9600, timeout=1)

# try:
#     while True:
#         line = ser_gps.readline().decode('ascii', errors='replace').strip()
#         if line.startswith('$GPGGA'):
#             if is_valid_gps_data(line):
#                 lat, lon = parse_gpgga(line)
#                 print(f"Latitude: {lat}, Longitude: {lon}")
#             else:
#                 print("Waiting for valid GPS data...")
# except KeyboardInterrupt:
#     print("Script interrupted by user")

# ser_gps.close()