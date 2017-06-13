#!/bin/bash
set -e


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
sudo pip3 install -r requirements.txt
sudo pip3 install -r requirements-hw.txt

echo "Downloading Speech Data for flite TTS"

if [ ! -f "cmu_us_slt.flitevox" ]
then
    wget "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_slt.flitevox"
fi

echo "Setup Complete"

echo "Run 'python3 main.py' to start"