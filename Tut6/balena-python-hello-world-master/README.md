## A Simple Server with Python Flask

This is a simple skeleton Flask server project that works on any of the devices supported by [balena][balena-link].

This project simply serves up a simple message ("EEE3095S Tutorial 6: By Luc van den Handel (VHNLUC001) and Sabrina Mackay (MCKSAB001) :)") on port `:80` of your balena device.

To get this project up and running, you will need to signup for a balena account [here][signup-page] and set up a device, have a look at our [Getting Started tutorial][gettingStarted-link]. Once you are set up with balena, you will need to clone this repo locally:
```
$ Setting up Device:
Use the Balena cloud services to set up your device and push this codebase to your fleet. Once that is done you can assign each device a public IP address which you can use to access the Flask server.
When you access the server (by typining in the IP and port into the URL bar of a web browser) you will see the simple message returned by the server.
For more information and a detailed guide see the links below.
```




[balena-link]:https://balena.io/
[signup-page]:https://dashboard.balena-cloud.com/signup
[gettingStarted-link]:http://balena.io/docs/learn/getting-started/
