from flask import Flask, send_file, render_template
import socket
import time
import os
import threading


app = Flask(__name__)
# global variable
record = False
readings = []
length = 0
count = 0
status = 1
t = time.localtime

TCP_IP = '172.20.10.3'
TCP_PORT = 8000
BUFFER_SIZE = 1024

# create the socket to receive data from Pi1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# route endpoint that resets the log and returns the base html
@app.route('/')
def route():
    os.system("rm src/sensorlog.csv")
    os.system("touch src/sensorlog.csv")
    file = open("src/sensorlog.csv", "w")
    t = time.localtime()
    st = "{:02d}".format(t.tm_mday) + "/" + "{:02d}".format(t.tm_mon) + "/" + str(t.tm_year) + " - " + "{:02d}".format(t.tm_hour+2) + ":" + "{:02d}".format(t.tm_min)  + "\n"
    file.write(st)
    file.close()
    return render_template("index.html")

# start endpoint that instructs the server to start saving data received
@app.route('/start')
def start():
    
    global record
    global count
    record = True
    print("Started Saving Readings")
    if count == 0:
        return render_template("index.html")
    else:
        filename = "index" + str(count) + ".html"
        return render_template(filename)

# stop endpoint that instructs the server to stop saving data
@app.route('/stop')
def stop():
    global record
    record = False
    print("Stopped Saving Readings")
    if count == 0:
        return render_template("index.html")
    else:
        filename = "index" + str(count) + ".html"
        return render_template(filename)

# get readings endpoint that creates a new html file with the data saved included and returns that html file
@app.route('/getreadings')
def getreading():
    global count
    count += 1
    # create new file
    filename = "src/templates/index" + str(count) + ".html"
    
    os.system("touch " + filename)
    # open the file
    file = open(filename, "w")

    # write the top half of the html to the file
    file.write("""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Index</title>
</head>

<body>
  <h1 style="color: blue">EEE3095S Practical 6</h1>
  <p>by Luc van den Handel (VHNLUC001) and Sabrina Mackay (MCKSAB001)</p>
  <p>Pi1 Status: Unknown</p>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/start">Start</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/stop">Stop</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/status">Check Status</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/download">Download</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/getreadings">Get Readings</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/exit">Exit</a>
  
  <p>Time | Temp Reading | Temp | Light Reading</p>
  <div style="background-color: aquamarine;">
    <p>""")
    
    # write the readings to the file
    if count == 0:
        file.write("None<br>")
    else:
        # write all the readings in the array
        for i in readings:
            file.write(i.replace(";", " | ") + "<br>")
    # write the last part of the html to the file
    file.write("""</p>
  </div>
  
  
</body>

</html>""")

    file.close()
    finfilename = "index" + str(count) + ".html"
    # return the new file
    return render_template(finfilename)

# download endpoint that sends the sensor log to the user
@app.route('/download')
def download():
    os.system("pwd")
    return send_file("sensorlog.csv", as_attachment=True)

# exit endpoint that just displayed the goodbye message
@app.route('/exit')
def exit():
    
    return "Cheerio! This session has ended, come back soon :)"

# check status endpoint that works similarly to get readings, just now we change the status test based on the time since the last reading
@app.route('/status')
def checkstatus():
    global t
    global count
    global status
    pt = time.localtime()
    # if it has been more than 2 minutes since we received data, then declare that Pi1 is offline (0)
    if pt.tm_min - t.tm_min >= 2:
        status = 0
    count += 1

    filename = "src/templates/index" + str(count) + ".html"
    
    os.system("touch " + filename)
    file = open(filename, "w")

    file.write("""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Index</title>
</head>

<body>
  <h1 style="color: blue">EEE3095S Practical 6</h1>
  <p>by Luc van den Handel (VHNLUC001) and Sabrina Mackay (MCKSAB001)</p>""")
    if status == 1:
        file.write("""<p>Pi1 Status: Online - Receiving data</p>""")
    else:
        file.write("""<p>Pi1 Status: Offline - Not receiving data</p>""")
  
    file.write("""<a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/start">Start</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/stop">Stop</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/status">Check Status</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/download">Download</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/getreadings">Get Readings</a>
  <a href="https://5ed128ab234cbd121f77236206f61be6.balena-devices.com/exit">Exit</a>
  
  <p>Time | Temp Reading | Temp | Light Reading</p>
  <div style="background-color: aquamarine;">
    <p>""")
    
    if count == 0:
        file.write("None<br>")
    else:
        for i in readings:
            file.write(i.replace(";", " | ") + "<br>")

    file.write("""</p>
  </div>
  
  
</body>

</html>""")

    file.close()
    finfilename = "index" + str(count) + ".html"
    return render_template(finfilename)

# function to run in a thread that receives data from Pi1
def receive():
    global record
    global readings
    global s
    global BUFFER_SIZE
    global length
    global t
    print("Started Thread")
    
    # loop endlessly
    while(True):
        
        print("Waiting for reading")
        # connect with Pi1
        conn, addr = s.accept()
        # receive reading from Pi1
        data = conn.recv(BUFFER_SIZE)
        read = data.decode()
        print("received reading:", read)
        # get the time received
        t = time.localtime()
        
        # addpend the time to the reading
        st = "{:02d}".format(t.tm_hour+2) + ":" + "{:02d}".format(t.tm_min) + ":" + "{:02d}".format(t.tm_sec)
        read = st + read
        # if we have started, save the reading
        if(record):
            file = open("src/sensorlog.csv", "a")
            # if we have less than 10 readings just append to list and save to file
            if(length < 10):
                readings.append(read)
                length += 1
                file.write(read + "\n")
                
            else:
            # else append to array and remove first element (only 10 in array) and save to file
                readings.append(read)
                readings.pop(0)
                file.write(read + "\n")
            file.close()


            


if __name__ == '__main__':
    os.system("pwd")
    # create new sensorlog file
    os.system("rm src/sensorlog.csv")
    os.system("touch src/sensorlog.csv")
    file = open("src/sensorlog.csv", "w")
    t = time.localtime()
    st = "{:02d}".format(t.tm_mday) + "/" + "{:02d}".format(t.tm_mon) + "/" + str(t.tm_year) + " - " + "{:02d}".format(t.tm_hour+2) + ":" + "{:02d}".format(t.tm_min) + "\n"
    file.write(st)
    file.close()
    
    # create and start the thread
    thread = threading.Thread(target=receive)
    thread.start()
    

    # start the server
    app.run(host='0.0.0.0', port=80)
