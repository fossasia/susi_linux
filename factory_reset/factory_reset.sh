#! /bin/bash
# To be executed using a physical button

cd $HOME/SUSI.AI/susi_linux
pwd
mv susi_linux/ susi_temp
git clone https://github.com/fossasia/susi_linux #while testing change to personal repo
pwd
ls
cd susi_linux

rm -rf ../susi_temp

./install.sh
