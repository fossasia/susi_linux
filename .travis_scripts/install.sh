#!/bin/bash
set -e

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

function install_swig_from_sources()
{
    wget https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz
    tar xf swig-3.0.12.tar.gz
    cd swig-3.0.12
    ./configure
    make
    sudo make install
    rm -rf swig-3.0.12*
    cd ..
}

function install_flite_from_source()
{
    wget http://www.festvox.org/flite/packed/flite-2.0/flite-2.0.0-release.tar.bz2
    tar xf flite-2.0.0-release.tar.bz2
    cd flite-2.0.0-release
    ./configure
    make
    sudo make install
    rm -rf flite-2.0.0-release*
    cd ..
}

function install_dependencies()
{
    if /usr/bin/dpkg --search /usr/bin/dpkg
    then
        if ! [ -x "$(command -v swig)" ]
        then
            install_swig_from_sources
        else
            installed_version=$(swig -version | perl -nae 'print "$F[2]\n" if /SWIG Version/i;')
            minimum_version="3.0.10"
            result=$(vercomp ${installed_version} ${minimum_version})
            if [ ${result} -eq 2 ]
            then
                echo "Installing SWIG 3.0.12 from sources"
                install_swig_from_sources
            else
                echo "SWIG version is up to date"
            fi
        fi
        sudo -E apt install libatlas-dev libatlas-base-dev
    else
        return 1;
    fi
}

function install_snowboy()
{
    if install_dependencies
    then
        root_dir=$(pwd)
        git clone https://github.com/Kitt-AI/snowboy.git
        cd snowboy/swig/Python3
        make -j4
        if [ -f _snowboydetect.so ]; then
            echo "Moving files"
            cp _snowboydetect.so ${root_dir}/main/hotword_engine/snowboy
            cp snowboydetect.py ${root_dir}/main/hotword_engine/snowboy
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

echo "Setup Complete"

echo "Run 'python3 -m main' to start"