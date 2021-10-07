import busio
import RPi.GPIO as GPIO
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import threading

#inital thread delay
delay=1.0

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

def setup():
    # Setup board mode
    # GPIO.setmode(GPIO.BOARD)
    # setup the push button
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(26, GPIO.FALLING, callback=btn_pressed, bouncetime=200)



#changes the delay time of the thread
def btn_pressed(channel):
    global delay
    if delay == 10.0:
        delay=5.0
    elif delay == 5.0:
        delay=1.0
    else:
        delay=10.0
	
def print_result():
    global delay
    global chan1
    global chan2
    n=time.time()-startTime
    seconds= str(round(n,0)) + "s"
    #sensor output at 0 degrees(V0) is 500mV and Ref voltage of the sensor is 5V and there are 1023 ADC levels
    #voltage output from the sensor = ADC_VALUE * (REF/LEVELS)
    voltage = chan1.value * (5.0/1023.0)
    #temperature: t = Senser voltage - 500mV
    t = str(round((voltage - 0.5), 2)) + "C"
    print("{0:<20} {1:<20} {2:<20} {3:<20}".format(seconds,chan1.value, t, chan2.value))
    time.sleep(delay)
    
if __name__ == "__main__":
    setup()
    print("{0:<20} {1:<20} {2:<20} {3:<20}".format("Runtime","Temp Reading", "Temp", "Light Reading"))
    startTime= time.time()
    while True:
        thread = threading.Thread(target=print_result)
        thread.start()
        thread.join()
