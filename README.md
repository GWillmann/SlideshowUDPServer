# Digital Photo Frame Project

## Made with <3 with a Raspberry Pi 3

[INSERT VIDEO/PICTURE HERE]

### Introduction

I have made a digital photo frame as a side project.
@See details [here](https://medium.com/@Gr3g0ire/un-cadre-photo-digital-19aee3bfddbc) (sorry in French for now) 
To simplify the control of the slideshow, I have written a quick app with React Native.

The server repo is ==> https://github.com/GWillmann/SlideshowUDPServer
The app repo is => https://github.com/GWillmann/SlideshowApp

This repo contains the code for server written in Python running on the raspberry

### Installation

Place *server.py* somewhere in your raspberry.
Change these values in *server.py*:
```python
PI_ADDRESS = '[IP ADDRESS OF YOUR RASPBERRY PI]'
SLIDESHOW_ROOT_FOLDER = '[PATH TO YOUR SLIDESHOW FOLDERS]'
```

To run it after every boot, append this line to the file *~/.bashrc*

```bash
python /home/pi/development/python/server.py &
```

### Thanks
This side project was greatly inspired by 

- https://github.com/tradle/react-native-udp 
- https://pymotw.com/2/socket/udp.html


Without thoses resources, it would probably have never seen the bright
lights of Github repos!

### License
<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
