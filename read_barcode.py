#!/usr/bin/python2
import serial

try:
    bcd = serial.Serial(port='/dev/ttyACM0',
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        xonxoff=False,
                        timeout=1)

except serial.serialutil.SerialException as e:
    print(e)
    exit(1)

# Activate reader
bcd.write("\x16T\x0d")

response = bcd.readline()
print("Read %2d bytes: %s" % (len(response), response))

# Deactivate reader
bcd.write("\x16U\x0d")

bcd.close()
