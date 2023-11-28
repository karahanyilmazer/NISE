# %%
import socket
import time

import serial
import csv
from datetime import datetime
import os
import numpy as np
#from shared_memory_dict import SharedMemoryDict

# %%
# Set up the server
int_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # Change this to the IP address of your server
port = 12348    # Choose a port number

int_socket.bind((host, port))
int_socket.listen(1)

# Replace with the IP address of ESP32
arduino_host = '192.168.43.241'# '192.168.227.207' # #'192.168.27.5'
# Replace with the port number used for Arduino communication
arduino_port = 25002

# Create socket connection
arduino_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
arduino_sock.connect((arduino_host, arduino_port))


curr_path = os.getcwd()
data_path = r'/home/muhammed/Desktop/NISE/csv_data'
os.chdir(data_path)
run_num = sum("run_decoder" in f_name for f_name in os.listdir()) + 1

print(f"Server listening on {host}:{port}")

# Accept a connection
client_socket, client_address = int_socket.accept()
print(f"Connection from {client_address}")

# Send a message to the client
#message_to_client = "Hello, client! How are you?"


# Row selection first
letter_dict = {
    'A': [1, 1, 1],
    'B': [1, 1, 2],
    'C': [1, 2, 1],
    'D': [1, 2, 2],
    'E': [1, 3, 1],
    'F': [1, 3, 2],
    'G': [1, 4, 1],
    'H': [1, 4, 2],
    'I': [2, 1, 1],
    'J': [2, 1, 2],
    'K': [2, 2, 1],
    'L': [2, 2, 2],
    'M': [2, 3, 1],
    'N': [2, 3, 2],
    'O': [2, 4, 1],
    'P': [2, 4, 2],
    'Q': [3, 1, 1],
    'R': [3, 1, 2],
    'S': [3, 2, 1],
    'T': [3, 2, 2],
    'U': [3, 3, 1],
    'V': [3, 3, 2],
    'W': [3, 4, 1],
    'X': [3, 4, 2],
    'Y': [4, 1, 1],
    'Z': [4, 1, 2],
    '.': [4, 2, 1],
    '?': [4, 2, 2],
    ' ': [4, 3, 1],
    'backspace': [4, 3, 2],
    'send': [4, 4, 1],
}




print('Connection Set')
# Wait for game initialization
time.sleep(1)

# Set up serial connection port
# port = serial.Serial('COM7', baudrate=115200)  # Windows
port = serial.Serial('/dev/ttyUSB0', baudrate=115200)  # Linux


# Shared memory for communicating between different scripts
#smd = SharedMemoryDict(name='msg', size=1024)
#smd['sensor'] = 0
#smd['sending'] = False

print('All Connections Completed')

useless_list = [[4, 4, 2]]
tmp = 0
buffer = []
bufferL = []
# counter = 0
# %%

csv_list = []

while True:
    try:
        # time.sleep(0.1)
        line = port.readline().decode('utf-8')
    except KeyboardInterrupt:
        with open(f'run_decoder_{run_num}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)
        os.chdir(curr_path)

        break

    
    # Split the line into individual sensor values
    sensor_values = line.split(',')

    try:
        sensorValue1, sensorValue2, sensorValue3, sensorValue4 = sensor_values
        # Convert to integer if necessary
        sensorValue1 = int(sensorValue1)
        sensorValue2 = int(sensorValue2)
        sensorValue3 = int(sensorValue3)
        sensorValue4 = int(sensorValue4)
        # sensorVal = np.array([sensorValue1, sensorValue2, sensorValue3, sensorValue4])
        sensorVal = [sensorValue1, sensorValue2, sensorValue3, sensorValue4]
    except ValueError:
        sensorVal = [0, 0, 0, 0]

    force_idx = 0

    for i, sensorV in enumerate(sensorVal):
        if int(sensorV) > 3000:
            force_idx = i + 1

    if tmp != 0:
        if force_idx == 0:
            tmp = 0
        else:
            force_idx = 0

    else:
        if force_idx != 0:
            tmp = 1
            buffer.append(force_idx)

        else:
            force_idx = 0
            tmp = 0

        if len(buffer) == 3:
            if buffer[0:3] in useless_list or buffer[2]==3 or buffer[2]==4:
                buffer = []

        if len(buffer) == 6:
            # if buffer[3:6] == ['3','4','2']: # For column selection first
            if buffer[3:6] == [4, 3, 2]: # For row selection first
                buffer = []

            elif buffer[3:6] in useless_list or buffer[5]==3 or buffer[5]==4:
                buffer = buffer[0:3]

            else:
                for key, val in letter_dict.items():
                    if val == buffer[0:3]:
                        print_str = (val, key, datetime.now())
                        print(print_str)
                        csv_list.append(print_str)

                str_arduino = ''.join(str(num) for num in buffer[0:3])
                arduino_sock.sendall(str_arduino.encode())
                buffer = buffer[3:6]
        

    if force_idx != 0:
        time.sleep(0.1)
        client_socket.sendall(force_idx.to_bytes(4, byteorder='big'))
        
# Close the sockets
client_socket.close()
int_socket.close()
# %%