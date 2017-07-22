#!/bin/bash
set -e

function install_dependencies()
{
    if /usr/bin/dpkg --search /usr/bin/dpkg
    then
        sudo apt install swig libatlas-dev libatlas-base-dev
    else
        ret 1;
    fi
}

function install_snowboy()
{
    if install_dependencies
    then
        root_dir=`pwd`
        git clone https://github.com/Kitt-AI/snowboy.git
        cd snowboy/swig/Python3
        make -j4
        if [ -f _snowboydetect.so ]; then
            echo "Moving files"
            cp _snowboydetect.so ${root_dir}/hotword_engine/snowboy
            cp snowboydetect.py ${root_dir}/hotword_engine/snowboy
        else
            echo "FAILED: Unable to make Snowboy Detect file. Please follow manual instructions at https://github.com/kitt-AI/snowboy"
            echo "You may also use PocketSphinx Detector if you are unable to install snowboy on your machine"
        fi
        cd "$root_dir"
    else
        echo "FAILED: Installation of Snowboy on your system is not supported presently. Please follow manual instructions at https://github.com/kitt-AI/snowboy"
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

echo "Downloading Python Dependencies"
pip3 install -r requirements.txt
pip3 install -r requirements-hw.txt

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

echo "Setup Complete"

echo "Run 'python3 main.py' to start"