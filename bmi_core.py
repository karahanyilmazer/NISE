# %%
import socket
import time

import serial
from shared_memory_dict import SharedMemoryDict

# %%
# UDP network
UDP_IP = "192.168.4.3"
UDP_PORT = 9999
MESSAGE = "000_000_000_000"
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP

# Shared memory for communicating between different scripts
# smd = SharedMemoryDict(name="msg", size=1024)
# smd["sensor_1"] = 0

number_vibros = 4
intensity_array = [0, 0, 0, 0]

port = serial.Serial("COM7", baudrate=115200)  # Windows
# port = serial.Serial('/dev/ttyUSB0')  # Linux

# %%
while True:
    # Get the message from ESP32 with IMU and EMG
    line = port.readline().decode("utf-8")

    # Split the line into individual sensor values
    sensor_values = line.split(",")
    try:
        sensorValue1, sensorValue2, sensorValue3, sensorValue4 = sensor_values
        # Convert to integer if necessary
        sensorValue1 = int(sensorValue1)
        sensorValue2 = int(sensorValue2)
        sensorValue3 = int(sensorValue3)
        sensorValue4 = int(sensorValue4)
    except ValueError:
        sensorValue1, sensorValue2, sensorValue3, sensorValue4 = 0,0,0,0


    print(sensorValue1, sensorValue2, sensorValue3, sensorValue4)

    # Send feedback intensities to ESP32 with vibrotactile motors
    # send_array_udp(intensity_array, number_vibros)

# %%
