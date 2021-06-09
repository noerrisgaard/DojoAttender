
![alt text](src/ui/assets/banner.png "Logo Title Text 1")
# DojoAttender

This project was made for my final exam during my education as a Data Technician specialized in programming.

There was a need for a system being able to track members attendance at my local martial arts club. I came up with this project.

The system is able to:
 * Register new members to the martial arts club
 * Analyze said new members face encodings
 * Record attencance for martial arts classes by facial recognition
 * Generate Excel sheets with attendance data and export to USB


___
## Hardware
 * [Raspberry Pi B 4GB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
 * [Raspberry Pi 7" Touch Display](https://www.raspberrypi.org/products/raspberry-pi-touch-display/)
 * [Raspberry Pi Camera Module v2](https://www.raspberrypi.org/products/camera-module-v2/)
 * [SmartiPi Touch 2 - Raspbery Pi Case](https://smarticase.com/collections/smartipi-touch-2/products/smartipi-touch-2)
___
 
## Software
I've used Debian (Buster) for this project.

Install the required python modules found in requirements.txt `pip install -r  requirements.txt`

### Automount USB
To be able to automount USB you need to install USBMount. As the version present in the Debian package manager is not working on this sytem, you need to download the newest version from the [repo](https://github.com/rbrito/usbmount) and install it from there.

### Autorun on boot
To be able to autorun the application on startup, `/etc/xdg/lxsession/LXDE-pi/autostart` has to be edited:

`@xscreensaver`  
`@/usr/bin/python3 /home/pi/workspace/DojoAttender/src/main.py`(Or path to wherever you saved main.py)

### Disable cursor
To disable cursor add `xserver-command=X -nocursor` to `/etc/lightdm/lightdm.conf`
___
Further installation of applications and requirements may be needed. If you inted to use this project, get in contact if you encounter any issues.