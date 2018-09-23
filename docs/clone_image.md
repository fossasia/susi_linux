# How to clone an existing image from one SD card to another

First you must insert your existing image to the usb reader and find out where it is mounted. On MacOS you write:
`diskutil list`

The result may be a list containing a section with your SD card. If the card is 16GB, it could look like this:
```
/dev/disk5 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *16.0 GB    disk5
   1:             Windows_FAT_32 boot                    45.3 MB    disk5s1
   2:                      Linux                         15.9 GB    disk5s2
```
This gives you the information that the sd card is mounted to the disk `/dev/disk5`

Then copy the whole card to your disk:

- First you must un-mount the sd card:

  `diskutil unmount /dev/disk5s1` 

- then copy the card:

  `sudo dd if=/dev/rdisk5 bs=16m | pv -s 16G > rpi_devstep0.img`

Copying a 16GB sd card takes about 10 minutes.
