#!/usr/bin/python

import os
from glob import glob
import shutil
from subprocess import check_output #nosec #pylint-disable type: ignore

def make_skill(): # pylint-enable
    name_of_usb = get_mount_points()
    print(type(name_of_usb))
    print(name_of_usb[0])
    x = name_of_usb[0]
    os.chdir('{}'.format(x[1]))
    USB = name_of_usb[0]
    mp3_files = [file for file in glob("*.mp3")]
    music_path = list()	
    for mp in mp3_files:	
        music_path.append("{}".format(USB[1]) + "/{}".format(mp))	
    f = open('/home/pi/SUSI.AI/susi_linux/media_daemon/custom_skill.txt','w+')
    f.close()
    song_list = " ".join(music_path)
    skills ='play audio \n !console:Playing audio from your usb device\n{"actions":\
    [ \n{"type":"audio_play", "identifier_type":"url",\
     "identifier":'+str(song_list)+'\n}\n]}'
    f1 = open('/home/pi/SUSI.AI/susi_linux/media_daemon/custom_skill.txt','w+')
    for skill in skills:
        f1.write(skill + '\n')
    shutil.move('/home/pi/SUSI.AI/susi_linux/media_daemon/custom_skill.txt','/home/pi/SUSI.AI/susi_linux/susi_server/susi_server/data/generic_skills/media_discovery')
    os.chdir('/home/pi/SUSI.AI/susi_linux/susi_server/susi_server/data/settings/')
    f2 = open('customized_config.properties','a')
    f2.write('local.mode = true')
    f2.close()
    os.chdir('/home/pi/SUSI.AI/susi_linux/')

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines() #nosec #pylint-disable type: ignore
    output = [tmp.decode('UTF-8') for tmp in output ] # pytlint-enable
    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]

if __name__ == '__main__':
    
    print(get_mount_points())
    name_of_usb = get_mount_points()
    print(type(name_of_usb))
    file = open('/home/pi/SUSI.AI/susi_linux/media_daemon/lmfzao.txt','w+')
    file.write('Hello World')
    
    file.write('Debug1')
    name_of_usb = get_mount_points()
    file.write('Debug2 \n')
    file.write('Debug3 \n')
    print('tmkc')
    USB = name_of_usb
    file.write('Debug4 \n')
    mp3 = [file for file in glob("*.mp3")]
    f = open('/home/pi/SUSI.AI/susi_linux/media_daemon/custom_skill.txt','w+')
    file.write('Debug5 \n')
    skills = ['play audio \n !console:Playing audio from your usb device \n']
    file.write('Debug6 \n')
    for skill in skills:
        f.write(skill)
    shutil.move('/home/pi/SUSI.AI/susi_linux/media_daemon/custom_skill.txt','/home/pi/SUSI.AI/susi_linux/susi_server/susi_server/data/generic_skills/media_discovery')
    os.chdir('/home/pi/SUSI.AI/susi_linux/susi_server/susi_server/data/settings/')
    f2 = open('customized_config.properties','a')
    f2.write('local.mode = true')
    f2.close()
    os.chdir('/home/pi/SUSI.AI/susi_linux/')
    