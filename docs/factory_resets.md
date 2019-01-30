# Factory Resets
[Factory Reset](../factory_reset/factory_reset.py)

Currently, our factory reset is configured on the GPIO port 17 of the Raspberry Pi, i.e. when the button configured to the port 17 or the one connected on the ReSpeaker Pi Hat is pressed for longer than 7 seconds, the factory reset [script](../factory_reset/factory_reset.sh) which moves the backup version of the software and deletes the original file.

## Future RoadMap
Deleting everything from the Speaker System is a very hard and robust way of reset-ing the speaker.
We expect to create a Soft Reset, which just uninstalls the packages and the local-server and re-installs them and hence providing a softer way of reset.
