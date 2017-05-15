#!/bin/bash
set -e

echo "Downloading dependency: Susi Python API Wrapper"
git clone https://github.com/fossasia/susi_api_wrapper.git

echo "setting correct location"
mv susi_api_wrapper/python_wrapper/susi_python susi_python
mv susi_api_wrapper/python_wrapper/requirements.txt requirements.txt

echo "Downloading Python Dependencies for Susi Python API Wrapper"
pip3 install -r requirements.txt

echo "Cleaning up"
rm -rf susi_api_wrapper

echo "Setup Complete"

echo "Run app.py to run"