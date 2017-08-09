#!/usr/bin/python2
import serial
import sys
import getopt

# Default arguments
device = "/dev/ttyACM0"
output = "output.jpg"

# Read command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "d:o:")

except getopt.GetoptError:
    print(sys.argv[0], "[-d] [-o]")
    print("d: Device (default=%s)", device)
    print("o: Output (default=%s)", output)
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-d"):
        device = arg
    elif opt in ("-o"):
        output = arg

# Open serial port
try:
    bcd = serial.Serial(port=device,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        xonxoff=False,
                        timeout=1)

except serial.serialutil.SerialException as e:
    print(e)
    exit(1)

# Take the picture
bcd.write("\x16M\x0dIMGSNP.\x0d")
r = bcd.readline()

# Transfer the image
bcd.write("\x16M\x0dIMGSHP.\x0d")
lines = bcd.readlines()

bcd.close()

# Concat the received lines to a single string
response = ""
for line in lines:
    response += line

print("Read %2d bytes" % len(response))

# Locate start of end of prefix
start = response.find("\x1d") + 1
print("Start:", start)

# Locate start of suffix
end = start + response[start:].find("IMGSHP")
print("End:", end)

# Write image to file
f = open(output, 'w')
f.write(response[start:end])
f.close()
