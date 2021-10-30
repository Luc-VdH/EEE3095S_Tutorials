## A Sensor Data Server with Python Flask

This is a Flask server project that works on any of the devices supported by [balena][balena-link].

The Flask server receives sensor data from a separate device and provides a webapp. The webapp allows the user to view the data received from the senor, download a log of the data, check the status of the sensor and stop and start the recording of data.

To get this project up and running, you will need to signup for a balena account [here][signup-page] and set up a device, have a look at our [Getting Started tutorial][gettingStarted-link]. Once you are set up with balena, you will need to clone this repo locally:
```
$ Setting up Device:
Use the Balena cloud services to set up your device and push this codebase to your fleet. Once that is done you can assign each device a public IP address which you can use to access the Flask server.
When you access the server (by typining in the IP and port into the URL bar of a web browser) you will see the simple message returned by the server.
If you have a sensor node running with the correct IP and port the server should start receiving data every 10 seconds. You can then control the saving of the data and view the data from the webapp which is accessed from the route endpoint. 
```




[balena-link]:https://balena.io/
[signup-page]:https://dashboard.balena-cloud.com/signup
[gettingStarted-link]:http://balena.io/docs/learn/getting-started/
