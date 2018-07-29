#! /bin/bash
# To be executed using a physical button

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cd $DIR_PATH/
pwd

sudo tar xvf $DIR_PATH/reset_folder.tar.gz  # extracting the backup folder
mv $DIR_PATH/../susi_linux $DIR_PATH/../../susi_temp  # moving the backup file as a temp file
mv $DIR_PATH/../../susi_linux $DIR_PATH/../../susi_temp2  # making the original file to a temp file to delete it
mv $DIR_PATH/../susi_temp $DIR_PATH/../../susi_linux  # making the backupfile as a new one

rm -rf $DIR_PATH/../../susi_temp2 # finally removing the file
