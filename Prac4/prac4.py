import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import threading

#inital thread delay
delay=10.0

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
    GPIO.setmode(GPIO.BOARD)
    # setup the push button
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=btn_pressed, bouncetime=200)


if __name__ == "__main__":
    setup()
    print("{0:<20} {1:<20} {2:<20} {3:<20}".format("Runtime","Temp Reading", "Temp", "Light Reading"))
    startTime= time.time()
    while True:
        thread = threading.Thread(target=print_result, args=(delay,))
        thread.start()
        thread.join()

#changes the delay time of the thread
def btn_pressed():
    if delay == 10.0:
        delay=5.0
    elif delay == 5.0:
        delay=1.0
    else:
        delay=10.0
	
def print_result():
    time.sleep(delay)
    n=time.time()-startTime
    seconds=n+"s"
    #sensor output at 0 degrees(V0) is 500V and the temperature co-efficient(Tc) is 10
    #temp=(Vdata-V0)/Tc
    temp=(chan1.value-500)/10
    print("{0:<20.0f} {1:<20} {2:<20}C {3:<20}".format(seconds,chan1.value, temp, chan2.value))
    
