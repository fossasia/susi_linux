
Setting up SUSI.AI for development on a desktop machine
=======================================================

Choose your own development place
```
DEVDIR=~/SUSI.AI
```

Install necessary packages
--------------------------

```
sudo apt-get install ca-certificates git openssl wget python3-setuptools perl libterm-readline-gnu-perl \
	python3-pip sox libsox-fmt-all flac libportaudio2 libatlas3-base libpulse0 libasound2 \
	vlc-bin vlc-plugin-base vlc-plugin-video-splitter python3-cairo python3-flask flite \
	openjdk-8-jdk-headless pixz udisks2 i2c-tools libasound2-plugins python3-dev \
	swig python3-requests python3-service-identity python3-pyaudio python3-levenshtein \
	python3-pafy python3-colorlog python3-watson-developer-cloud libpulse-dev libasound2-dev \
	libatlas-base-dev
```

On Debian/stretch add vlc-nox at least


Install snowboy
---------------

We install snowboy from the Github release. The only useful fix is to
correctly identify the version in the pip install cache
```
cd $DEVDIR
wget https://github.com/Kitt-AI/snowboy/archive/v1.3.0.tar.gz
tar -xf v1.3.0.tar.gz
cd snowboy-1.3.0
sed -u -e "s/version='1\.2\.0b1'/version='1.3.0'/" setup.py
python3 setup.py build
sudo python3 setup.py install
cd ..
rm -rf snowboy-1.3.0 v1.3.0.tar.gz
```


Install SUSI.AI
---------------

Get various repositories (replace with `https://github.com/fossasia/...` for anonymous checkout)
```
cd $DEVDIR
git clone git@github.com:fossasia/susi_linux.git
git clone git@github.com:fossasia/susi_api_wrapper.git
git clone git@github.com:fossasia/susi_server.git
git clone git@github.com:fossasia/susi_skill_data.git
```

Update `susi_server` git submodules
```
cd $DEVDIR
cd susi_server
git submodule update --recursive --remote
git submodule update --init --recursive
```

We need to link a directory from `susi_api_wrapper` to `susi_linux`.
We also add this link to the ignored files of git:
```
cd $DEVDIR
ln -s ../susi_api_wrapper/python_wrapper/susi_python susi_linux/
echo "/susi_python" >> susi_linux/.git/info/exclude
```

Install other necessary pip modules
-----------------------------------
If you are on stretch, first upgrade pip and wheel
```
sudo pip3 install -U pip wheel
```

then
```
cd $DEVDIR
sudo pip3 install -r susi_api_wrapper/python_wrapper/requirements.txt
# these are the reqs from sus_linux/requirements-hw.txt adjusted and cleaned
sudo pip3 install pip3 install speechRecognition==3.8.1 service_identity pocketsphinx==0.1.15 pyaudio json_config google_speech async_promises python-Levenshtein pyalsaaudio 'youtube-dl>2018' python-vlc pafy colorlog rx
sudo pip3 install -r susi_linux/requirements-special.txt
```

Download speech sata for flite TTS
-----------------------------------
We need to get the TTS data files
```
cd $DEVDIR
cd susi_linux
if [ ! -f "extras/cmu_us_slt.flitevox" ]
then
    wget "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_slt.flitevox" -P extras
fi
```

Optional: update youtube.lua
----------------------------
Probably only on stretch, it might be necessary to update youtube.lua
```
cd $DEVDIR
wget https://raw.githubusercontent.com/videolan/vlc/master/share/lua/playlist/youtube.lua
sudo mv youtube.lua /usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)/vlc/lua/playlist/youtube.luac
```


Build `susi_server`
-------------------
```
cd $DEVDIR
cd susi_server
./gradlew build
```

Run `susi_server`
-----------------
```
cd $DEVDIR
cd susi_server
./bin/start.sh
```

Run `susi_linux`
----------------
```
cd $DEVDIR
cd susi_linux
python3 -m main -vv
```

