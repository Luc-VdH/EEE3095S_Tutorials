## A Temperature and Light Sensor Node

This is a sensor that connects to an ADC that reads temperature and light readings that works on any of the devices supported by [balena][balena-link].

This project requires a companion server that receives the data sent, the server will handle displaying and saving the data. This part of the project is just a sensor that takes a reading every 10 seconds and sends it to the server

To get this project up and running, you will need to signup for a balena account [here][signup-page] and set up a device, have a look at our [Getting Started tutorial][gettingStarted-link]. Once you are set up with balena, you will need to clone this repo locally:
```
$ Setting up Device:
Use the Balena cloud services to set up your device and push this codebase to your fleet. Once that is done you will need to replace the IP address with that of a server device also setup with Balena. 
The sensor will then start taking readings and sending data to the server, by default the server needs to listen on port 8000 but this can also be changed. 

```




[balena-link]:https://balena.io/
[signup-page]:https://dashboard.balena-cloud.com/signup
[gettingStarted-link]:http://balena.io/docs/learn/getting-started/
