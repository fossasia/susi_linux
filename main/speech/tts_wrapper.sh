#!/bin/bash
# This script is the wrapper script for TTS.
# This script is required to process multiple queries simultanously

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

python3 $DIR_PATH/TTS.py $1 $2
