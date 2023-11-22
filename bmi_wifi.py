# %%
import socket
import time

import serial
from shared_memory_dict import SharedMemoryDict

# %%
# # Function for sending command in binary mode
# def send_command(command):
#     # Send the command over the socket connection
#     arduino_sock.sendall(command.encode())


# Replace with the IP address of ESP32
arduino_host = '192.168.43.223'
# Replace with the port number used for Arduino communication
arduino_port = 25002

# Create socket connection
# arduino_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# arduino_sock.connect((arduino_host, arduino_port))

# Wait for game initialization
time.sleep(3)

# Set up serial connection port
port = serial.Serial('COM5', baudrate=115200)  # Windows

# Shared memory for communicating between different scripts
smd = SharedMemoryDict(name='msg', size=1024)
smd['sensor_1'] = 0
smd['sensor_2'] = 0
smd['sensor_3'] = 0
smd['sensor_4'] = 0

# %%
while True:
    try:
        line = port.readline().decode('utf-8')
    except KeyboardInterrupt:
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
        sensorVal = [sensorValue1, sensorValue2, sensorValue3, sensorValue4]
    except ValueError:
        # sensorValue1, sensorValue2, sensorValue3, sensorValue4 = 0,0,0,0
        sensorVal = [0, 0, 0, 0]

    sender = '0'
    for i, sensorV in enumerate(sensorVal):
        if int(sensorV) > 1500:
            sender = str(i + 1)
            smd[f'sensor_{i + 1}'] = 1
        else:
            smd[f'sensor_{i + 1}'] = 0

    # send_command(sensorValue1, sensorValue2, sensorValue3, sensorValue4)
    # send_command(sender)
    # print(sender)

# %%