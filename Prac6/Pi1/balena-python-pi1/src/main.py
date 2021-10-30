import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import socket
import threading

# inital thread delay
delay = 10.0

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 1 for temperature sensor
chan1 = AnalogIn(mcp, MCP.P1)

# create an analog input channel on pin 2 for light sensor
chan2 = AnalogIn(mcp, MCP.P2)
TCP_IP = '172.20.10.3'
TCP_PORT = 8000
BUFFER_SIZE = 1024



def print_result():
    global delay
    global chan1
    global chan2

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    n = time.time() - startTime
    seconds = str(round(n, 0)) + "s"
    # sensor output at 0 degrees(V0) is 500mV and Ref voltage of the sensor is 5V and there are 1023 ADC levels
    # voltage output from the sensor = ADC_VALUE * (REF/LEVELS)
    voltage = chan1.value * (5.0 / 1023.0)
    # temperature: t = Senser voltage - 500mV
    t = str(round((voltage - 0.5), 2)) + "C"
    data = ";{0:<20};{1:<20};{2:<20}".format(chan1.value, t, chan2.value)
    print(data)
    # encode data and send it to Pi2
    s.send(data.encode())
    s.close()
    print("data sent")
    # delay for 10 secs
    time.sleep(delay)


if __name__ == "__main__":
    
    print("{0:<20} {1:<20} {2:<20} {3:<20}".format("Runtime", "Temp Reading", "Temp", "Light Reading"))
    startTime = time.time()
    while True:
        thread = threading.Thread(target=print_result)
        thread.start()
        thread.join()
