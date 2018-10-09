## The SUSI.AI Development DIY Kit
This is a short tutorial to get started with the parts of the SUSI.AI development kit.
You should have the following parts:

* A Raspberry Pi 3 Model B+
* A ReSpeaker 2-Mics Pi HAT
* A speaker (like Audiocore AC870) with attached JST PH 2.0 2-Pin cable
* A 3D-printed SUSI.AI Faceplate - or DIY print from https://www.thingiverse.com/thing:3124755
* A 16GB SD card with pre-flashed OS - or DIY flash from https://github.com/fossasia/susi_linux/releases/tag/0.3
* 4x 3cm spacers, 4x 2.5mm nuts, 4x 2.5mm screws, 4x 3mm screws, 4x washer, 4x 3mm nuts

### What do you require to assemble the device
* A small crosstip/philips screwdriver
* Gripping pliers

### What else do you require to operate the device
* A Wifi hotspot and the access credentials
* A mobile phone (only android tested successfully so far)
* USB power/charger and cable

### What you should do first
* If your SD card has no image on it: download and flash
* If your SD card has an image on it: make a copy of the OS from the SD card: i.e.<br/>`sudo dd if=/dev/rdisk5 bs=16m | pv -s 16G > rpi_devstep0.img`

### Installation
The device needs an internet connection to work. To configure the device to use the wifi connection,
a pairing process is started on the mobile phone:
* Download and install the SUSI.AI App from https://github.com/fossasia/susi_android/releases/tag/1.1
* First you need an account on http://susi.ai - follow the instructions in the mobile app
* attach the SUSI.AI speaker to USB power and wait that it boots up.
* Connect the device with the app: Open Settings, Connect the speaker, Wait for re-boot of the speaker.

### Usage
* To speak to the SUSI.AI speaker, say 'susi' and wait for the 'bing' sound
* After you hear the sound, talk to susi.
