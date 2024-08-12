import serial
import serial.tools.list_ports
import time

def find_gps_ports(description_keyword="SimTech"):
    ports = serial.tools.list_ports.comports()
    matching_ports = []
    for port in ports:
        print(f"Checking port {port.device}: {port.description}")
        if description_keyword in port.description:
            matching_ports.append(port.device)
    return matching_ports

def send_at_command(ser, command, delay=2):
    print(f"Sending command: {command}")
    ser.write((command + '\r\n').encode())
    time.sleep(delay)
    response = ser.read_all().decode()
    print(f"Received response: {response}")
    return response

def is_valid_gps_response(response):
    nmea_sentences = ['$GNGNS', '$GPGGA', '$GPRMC']
    for sentence in nmea_sentences:
        if sentence in response:
            return True
    return False

def ddm_to_dd(degrees_minutes):
    d, m = divmod(float(degrees_minutes), 100)
    return d + (m / 60)

def parse_gpgga(sentence):
    fields = sentence.split(',')
    lat_ddm = fields[2]
    lon_ddm = fields[4]
    lat_dir = fields[3]
    lon_dir = fields[5]

    lat_dd = ddm_to_dd(lat_ddm)
    lon_dd = ddm_to_dd(lon_ddm)

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