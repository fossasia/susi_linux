import os
from glob import glob
import shutil
import subprocess #nosec #pylint-disable type: ignore
from mount import *

# To get media_daemon folder
media_daemon_folder = os.path.dirname(os.path.abspath(__file__))
base_folder = os.path.dirname(media_daemon_folder)
server_skill_folder = os.path.join(base_folder, 'susi_server/susi_server/data/generic_skills/media_discovery')
server_settings_folder = os.path.join(base_folder, 'susi_server/susi_server/data/settings')
server_restart_folder = os.path.join(base_folder, 'susi_server/susi_server/bin/restart.sh')

def make_skill(): # pylint-enable
    devices = list_media_devices()
    path = get_media_path(devices[0])
    subprocess.call(['udisks','mount',path])
    name_of_usb = get_mount_points()
    USB = name_of_usb[1]
    os.chdir(str(USB))
    mp3_files = glob("*.mp3")
    f = open( media_daemon_folder +'/custom_skill.txt','w')
    music_path = list()
    for mp in mp3_files:
        music_path.append("{}".format(USB) + "/{}".format(mp))

    song_list = " ".join(music_path)
    skills = ['play audio','!console:Playing audio from your usb device','{"actions":[','{"type":"audio_play", "identifier_type":"url", "identifier":"file://'+str(song_list) +'"}',']}','eol']
    for skill in skills:
        f.write(skill + '\n')
    f.close()
    shutil.move(os.path.join(media_daemon_folder, 'custom_skill.txt'), server_skill_folder)
    with open(os.path.join(server_settings_folder, 'customized_config.properties'), 'a') as f2:
        f2.write('local.mode = true')
    subprocess.call(['sudo','bash',server_restart_folder])

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])	
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = subprocess.check_output(['mount']).splitlines() #nosec #pylint-disable type: ignore
    output = [tmp.decode('UTF-8') for tmp in output ] # pytlint-enable
    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]

if __name__ == '__main__':
    make_skill()
