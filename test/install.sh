#!/bin/bash
set -e


add_fossasia_repo() {
    echo "Set pip repo for root"
    if ! sudo test -d /root/.pip; then sudo mkdir /root/.pip; fi
    echo -e "[global]\nextra-index-url=https://repo.fury.io/fossasia/" | sudo tee /root/.pip/pip.conf
    echo "Set pip repo for current user"
    if [ ! -d ~/.config/pip ]; then mkdir -p ~/.config/pip ; fi
    echo -e "[global]\nextra-index-url=https://repo.fury.io/fossasia/" > ~/.config/pip/pip.conf
}

add_debian_repo() {
    echo "Add ReSpeaker Debian repo"
    # Respeaker driver https://github.com/respeaker/deb
    wget -qO- http://respeaker.io/deb/public.key | sudo apt-key add -
    echo "deb http://respeaker.io/deb/ stretch main" | sudo tee /etc/apt/sources.list.d/respeaker.list
    sudo apt update
}

install_debian_dependencies()
{
    sudo -E apt install -y build-essential python3-pip sox libsox-fmt-all flac pulseaudio libpulse-dev \
    python3-cairo python3-flask mpv flite ca-certificates-java
    # We specify ca-certificates-java instead of openjdk-(8/9)-jre-headless, so that it will pull the
    # appropriate version of JRE-headless, which can be 8 or 9, depending on ARM6 or ARM7 platform.
}

function install_seed_voicecard_driver()
{
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
    install_seed_voicecard_driver
}

####  Main  ####
add_fossasia_repo
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

echo "Installing Python Dependencies"
sudo -H pip3 install -U pip wheel
pip3 install -r requirements.txt  # This is from susi_api_wrapper
pip3 install -r requirements-hw.txt
pip3 install -r requirements-special.txt

echo "Downloading Speech Data for flite TTS"

if [ ! -f "extras/cmu_us_slt.flitevox" ]
then
    wget "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_slt.flitevox" -P extras
fi
