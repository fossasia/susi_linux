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
    mount(devices[0])  # requires sudo permission
    os.chdir(str(path))
    mp3_files = glob("*.mp3")
    f = open( media_daemon_folder +'/custom_skill.txt','w')
    music_path = list()
    for mp in mp3_files:
        music_path.append("{}".format(path) + "/{}".format(mp))

    song_list = " ".join(music_path)
    skills = ['play audio','!console:Playing audio from your usb device','{"actions":[','{"type":"audio_play", "identifier_type":"url", "identifier":"file://'+str(song_list) +'"}',']}','eol']
    for skill in skills:
        f.write(skill + '\n')
    f.close()
    shutil.move(os.path.join(media_daemon_folder, 'custom_skill.txt'), server_skill_folder)
    with open(os.path.join(server_settings_folder, 'customized_config.properties'), 'a') as f2:
        f2.write('local.mode = true')
    subprocess.call(['sudo','bash',server_restart_folder])

if __name__ == '__main__':
    make_skill()
