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
    mp3 = [file for file in glob("*.mp3")]
    os.chdir('/home/pi/SUSI.AI/susi_linux/media_daemon/')
    f = open('custom_skill.txt','w')
    skills = ['play audio','!console:Playing audio from your usb device','{"actions":[','{"type":"audio_play", "identifier_type":"url", "identifier":"file://{}/{}"}'.format(USB[1],mp3[0]),']}','eol']
    for skill in skills:
        f.write(skill + '\n')
    f.close()
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
    make_skill()
