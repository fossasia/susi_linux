# Media Discovery Daemon
<p>
The Media Discovery Daemon is the daemon that we are using to detect whether a USB device is connected to the pi or not. To start the daemon, `media_daemon.sh` file is triggered on bootup or can be executed manually. This will check a new USB connection.
</p>
<p>
If a new USB connection is detected, the python script `auto_skills.py` is triggered which creates a custom skill in the SUSI server and allows the user to play music from the USB device. But if the USB device is removed, the skill file is removed and the server functions normally.
<p/>

<p>
The `autostart.sh` acts as a starting point for executing the `auto_skills.py` which in turn creates the custom skill under '$HOME/SUSI.AI/susi_linux/susi_server/susi_server/data/generic_skills/media_discovery/' as custom_skill.txt . The custom skill contains a JSON response of the audio play skill with file identifiers USB name and mp3 file name.
The custom_skill.txt is removed from the directory path when the `autostop.sh` gets executed.
</p>  

Libraries/ Modules used in the package
We are using:
* `udev` lib to monitor the status of the USB connection
* `shutil` module to move files from one directory to another
* `glob` module to traverse through the files in a specific directory


## Workflow


<img src="/docs/images/media_daemon.svg">
