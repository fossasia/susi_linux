#! /bin/bash
# To be executed using a physical button

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cd $DIR_PATH/../..
pwd
mv susi_linux/ susi_temp
git clone https://github.com/fossasia/susi_linux #while testing change to personal repo
pwd
ls
cd susi_linux

rm -rf ../susi_temp

./install.sh
