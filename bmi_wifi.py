# %%
import socket
import time

import serial
#from shared_memory_dict import SharedMemoryDict

# %%
# # Function for sending command in binary mode
def send_command(command):
    # Send the command over the socket connection
    arduino_sock.sendall(command.encode())

import socket

# Set up the server
int_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # Change this to the IP address of your server
port = 12345         # Choose a port number

int_socket.bind((host, port))
int_socket.listen(1)

print(f"Server listening on {host}:{port}")

# Accept a connection
client_socket, client_address = int_socket.accept()
print(f"Connection from {client_address}")

# Send a message to the client
#message_to_client = "Hello, client! How are you?"






# Replace with the IP address of ESP32
arduino_host = '192.168.27.5' #'192.168.43.223'
# Replace with the port number used for Arduino communication
arduino_port = 25002


# Create socket connection
arduino_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
arduino_sock.connect((arduino_host, arduino_port))
print('Connection Set')
# Wait for game initialization
time.sleep(3)

# Set up serial connection port
port = serial.Serial('COM7', baudrate=115200)  # Windows
# port = serial.Serial('/dev/ttyUSB0', baudrate=115200)  # Linux


# Shared memory for communicating between different scripts
#smd = SharedMemoryDict(name='msg', size=1024)
#smd['sensor'] = 0
#smd['sending'] = False

print('flamina')
shooter = 0
letter = []
# counter = 0
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

    interm = '0'
    for i, sensorV in enumerate(sensorVal):
        if int(sensorV) > 2500:
            interm = str(i + 1)

        

    # past_ind = interm

    if shooter != 0:
        if int(interm) == 0:
            shooter = 0
        else:
            sender = 0

    else:
        if int(interm) != 0:
            sender = int(interm)
            shooter = 1
            letter.append(interm)

        else:
            sender = 0
            shooter = 0

        if len(letter) == 6:
            # send_command(letter)
            if letter[3:6] == ['4','4','1']:
                letter = letter[0:3]
            # elif letter[3:6] == ['3','4','2']:
            else:
                letter = []
            # print(letter)
            send_command(''.join(letter))
            # print(''.join(letter))
            letter = []

    # print(letter)
    #smd['sensor'] = sender

    
    #if smd['sending'] == True:
    ##  send_command(sensorValue1, sensorValue2, sensorValue3, sensorValue4)
        # send_command(interm)
        
    if sender != 0:
        client_socket.sendall(sender.to_bytes(4, byteorder='big'))
        # print(sender)

# Close the sockets
client_socket.close()
int_socket.close()
# %%