#!/bin/bash
set -e
SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)


add_debian_repo() {
sudo apt update
}

install_debian_dependencies()
{
sudo -E apt install -y python3-pip sox libsox-fmt-all flac \
libportaudio2 libatlas3-base libpulse0 libasound2 \
python3-cairo python3-flask mpv flite ca-certificates-java pixz udisks2
# We specify ca-certificates-java instead of openjdk-(8/9)-jre-headless, so that it will pull the
# appropriate version of JRE-headless, which can be 8 or 9, depending on ARM6 or ARM7 platform.
# libatlas3-base is to provide libf77blas.so, liblapack_atlas.so for snowboy.
# libportaudio2 is to provide libportaudio.so for PyAudio, which is snowboy's dependency.

# TODO: Replace mpv with something else which doesn't pull video-related stuff.
}

function install_seeed_voicecard_driver()
{
# TODO: Modify this driver install script, so that it won't pull libasound-plugins,
# which in turn, pull lot of video-related stuff.
if arecord -l | grep -q voicecard
then
echo "ReSpeaker Mic Array driver was already installed."
return 0
fi
echo "installing Respeaker Mic Array drivers from source"
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
cd ..
tar czf ~/seeed-voicecard.tar.gz seeed-voicecard
rm -rf seeed-voicecard
}

function install_dependencies()
{
install_seeed_voicecard_driver
}

function install_susi_server() {
if  [ ! -d "susi_server" ]; then mkdir $DIR_PATH/susi_server; fi

SUSI_SERVER_PATH=$DIR_PATH/susi_server/susi_server
if [ ! -d $SUSI_SERVER_PATH ]
then
git clone --recurse-submodules https://github.com/fossasia/susi_server.git $SUSI_SERVER_PATH
# The .git folder is big. Delete it (we don't do susi_server deveplopment here, so no need to keep it)
echo "Delete $SUSI_SERVER_PATH/.git"
rm -rf $SUSI_SERVER_PATH/.git
fi

SKILL_DATA_PATH=$DIR_PATH/susi_server/susi_skill_data
if [ ! -d $SKILL_DATA_PATH ]
then
git clone https://github.com/fossasia/susi_skill_data.git $SKILL_DATA_PATH
fi

if [ -d $SUSI_SERVER_PATH ]
then
echo "Deploying local SUSI server"
cd $SUSI_SERVER_PATH
{
./gradlew build
# Stop Gradle daemons after building
./gradlew --stop
} || {
echo PASS
}
fi
}

disable_ipv6_avahi() {
# Avahi has bug with IPv6, and make it fail to propage mDNS domain.
sed -i 's/use-ipv6=yes/use-ipv6=no/g' /etc/avahi/avahi-daemon.conf
}


####  Main  ####
add_debian_repo

echo "Downloading dependency: Susi Python API Wrapper"
if [ ! -d "susi_python" ]
then
git clone https://github.com/fossasia/susi_api_wrapper.git

echo "setting correct location"
mv susi_api_wrapper/python_wrapper/susi_python susi_python
mv susi_api_wrapper/python_wrapper/requirements.txt requirements.txt
rm -rf susi_api_wrapper
fi

echo "Installing required Debian Packages"
install_debian_dependencies
install_dependencies
disable_ipv6_avahi

echo "Installing Python Dependencies"
# We don't use "sudo -H pip3" here, so that pip3 cannot store cache.
# We want to discard cache to save disk space.
sudo pip3 install -U pip wheel
sudo pip3 install -r requirements.txt  # This is from susi_api_wrapper
sudo pip3 install -r requirements-hw.txt
sudo pip3 install -r requirements-special.txt

echo "Downloading Speech Data for flite TTS"

if [ ! -f "extras/cmu_us_slt.flitevox" ]
then
wget "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_slt.flitevox" -P extras
fi

echo
echo "NOTE: Snowboy is not compatible with all systems. If the setup indicates failed, use PocketSphinx engine for Hotword"
echo

echo "Updating the Udev Rules"
cd $DIR_PATH
sudo ./media_daemon/media_udev_rule.sh

echo "Cloning and building SUSI server"
install_susi_server

echo "Updating Systemd Rules"
sudo bash $DIR_PATH/Deploy/auto_boot.sh

cd $DIR_PATH
echo "Creating a backup folder for future factory_reset"
tar -I 'pixz -p 2' -cf ../reset_folder.tar.xz --checkpoint=.1000 -C .. susi_linux
echo ""  # To add newline after tar's last checkpoint
mv ../reset_folder.tar.xz $DIR_PATH/factory_reset/reset_folder.tar.xz

echo "Converting RasPi into an Access Point"
sudo bash $DIR_PATH/access_point/wap.sh
