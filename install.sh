#!/bin/bash
set -e
SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

install_debian_dependencies()
{
    sudo -E apt install -y swig build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev \
    libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libssl-dev libffi-dev \
    python-dev python3-dev python3-pip sox libsox-fmt-all flac portaudio19-dev pulseaudio libpulse-dev \
    python3-cairo python3-flask mpv
}

# Implementation from https://stackoverflow.com/questions/4023830/how-compare-two-strings-in-dot-separated-version-format-in-bash
vercomp()
{
    if [[ $1 == $2 ]]
    then
        echo 0;
        return 0;
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            echo 1;
            return 0;
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            echo 2;
            return 0;
        fi
    done
    echo 0;
}


function install_seed_voicecard_driver()
{
    echo "installing Respeaker Mic Array drivers from source"
    git clone https://github.com/respeaker/seeed-voicecard.git
    cd seeed-voicecard
    sudo ./install.sh
    cd ..
    mv seeed-voicecard ~/seeed-voicecard
}

function install_flite_from_source()
{
    wget http://www.festvox.org/flite/packed/flite-2.0/flite-2.0.0-release.tar.bz2
    tar xf flite-2.0.0-release.tar.bz2
    cd flite-2.0.0-release
    ./configure
    make
    sudo make install
    cd ..
    rm -rf flite-2.0.0-release*
}

function install_dependencies()
{
    install_seed_voicecard_driver
    if /usr/bin/dpkg --search /usr/bin/dpkg
    then
        sudo -E apt install -y libatlas-base-dev
    else
        return 1;
    fi
}

function install_snowboy()
{
    if install_dependencies
    then
        root_dir=$(pwd)
        sudo pip3 install git+https://github.com/Kitt-AI/snowboy.git
        if [ $? -ne 0 ]; then
            echo "FAILED: Unable to make Snowboy Detect file. Please follow manual instructions at https://github.com/kitt-AI/snowboy"
            echo "You may also use PocketSphinx Detector if you are unable to install snowboy on your machine"
        else
            echo "Snowboy Detect successfully installed"
        fi
        cd "$root_dir"
        rm -rf snowboy
    else
        echo "FAILED: Installation of Snowboy on your system is not supported presently. Please follow manual instructions at https://github.com/kitt-AI/snowboy"
    fi
}



function susi_server(){
    if  [ ! -d "susi_server" ]
    then
        mkdir $DIR_PATH/susi_server
        cd $DIR_PATH/susi_server
        git clone https://github.com/fossasia/susi_server.git
        git clone https://github.com/fossasia/susi_skill_data.git
    fi

    if [ -d "susi_server" ]
    then
        echo "Deploying local server"
        cd $DIR_PATH/susi_server/susi_server
        git submodule update --recursive --remote
        git submodule update --init --recursive
        {
            ./gradlew build
        } || {
            echo PASS
        }

        bin/start.sh
    fi
}

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

echo "Downloading Python Dependencies"
pip3 install -r requirements.txt
sudo -E -H pip3 install -r requirements-hw.txt


if ! [ -x "$(command -v flite)" ]
then
    echo "Downloading and Installing Flite TTS"
    install_flite_from_source
fi

echo "Downloading Speech Data for flite TTS"

if [ ! -f "extras/cmu_us_slt.flitevox" ]
then
    wget "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_slt.flitevox"
    mv cmu_us_slt.flitevox extras/
fi

echo "Setting up Snowboy"
echo
echo
echo "NOTE: Snowboy is not compatible with all systems. If the setup indicates failed, use PocketSphinx engine for Hotword"
echo
echo

install_snowboy

cd $DIR_PATH
sudo ./media_daemon/media_udev_rule.sh

echo "Cloning and building SUSI server"
susi_server

echo -e "\033[0;92mSUSI is installed successfully!\033[0m"
echo -e "Run configuration script by 'python3 config_generator.py \033[0;32m<stt engine> \033[0;33m<tts engine> \033[0;34m<snowboy or pocketsphinx> \033[0;35m<wake button?>' \033[0m"
echo "For example, to configure SUSI as following: "
echo -e "\t \033[0;32m-Google for speech-to-text"
echo -e "\t \033[0;33m-Google for text-to-speech"
echo -e "\t \033[0;34m-Use snowboy for hot-word detection"
echo -e "\t \033[0;35m-Do not use GPIO for wake button\033[0m"
echo -e "python3 config_generator.py \033[0;32mgoogle \033[0;33mgoogle \033[0;34my \033[0;35mn \033[0m"
