import serial
from sys import exit

PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

ser = None
try:
    ser = serial.Serial(PORT, BAUD_RATE)
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            tokens = line.split(',')
            print(f"Quaternion: {tokens[0]}, {tokens[1]}, {tokens[2]}, {tokens[3]}")
            print(f"Acceleration: {tokens[4]}, {tokens[5]}, {tokens[6]}")
            print()
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print("Error opening serial port: " + str(e))
    exit(1)
finally:
    if ser and ser.is_open:
        ser.close()