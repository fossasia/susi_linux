#!/bin/sh
# To be configured at bootup

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")
CHECK=''
if [ $LOCAL = $REMOTE ]
then
    echo "Up-to-date"
    CHECK='up-to-date'
elif [ $LOCAL = $BASE ] 
then
    echo "Need to pull"
    CHECK='Need-to-pull'
else
    echo "Diverged"
fi

if [$CHECK = "Need-to-pull"]
then
    git fetch UPSTREAM
    git merge UPSTREAM/master
fi
