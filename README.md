# SUSI AI on Linux

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/167b701c744841c5a05269d06b863732)](https://app.codacy.com/app/fossasia/susi_linux?utm_source=github.com&utm_medium=referral&utm_content=fossasia/susi_linux&utm_campaign=badger)
[![Build Status](https://travis-ci.org/fossasia/susi_linux.svg?branch=master)](https://travis-ci.org/fossasia/susi_linux)
[![Join the chat at https://gitter.im/fossasia/susi_hardware](https://badges.gitter.im/fossasia/susi_hardware.svg)](https://gitter.im/fossasia/susi_hardware?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Twitter Follow](https://img.shields.io/twitter/follow/susiai_.svg?style=social&label=Follow&maxAge=2592000?style=flat-square)](https://twitter.com/susiai_)

SUSI.AI Linux an implementation of SUSI.AI capable to run on Linux computers and Linux devices in headless mode. It can be installed on smart speakers, desktop PCs, Linux capable IoT devices, car system, washing machines and more.

## Project Overview 

The whole SUSI.AI ecosystem consists of the following parts:
```
 * server back-end
 |_ susi_server        (the brain of the infrastructure, a server which computes answers from queries)
 |_ susi_skill_data    (the knowledge of the brain, a large collection of skills provided by the SUSI.AI community)
 
 * android front-end
 |_ susi_android       (Android application which is a client for the susi_server at https://api.susi.ai)
 
 * iOS front-end
 |_ susi_iOS           (iOS application which is a client for the susi_server at https://api.susi.ai)
 
 * Content Management System for the SUSI.AI Skills - Home of the SUSI.AI community
 |_ accounts.susi.ai   (React Application, User Account Management for the CMS)
 |_ chat.susi.ai       (React Application, a client for the susi_server at https://api.susi.ai)
 |_ susi_skill_cms     (React Application, the content management system for susi skills)
 
 * Smart Speaker - Software to turn a Raspberry Pi into a Personal Assistant
 | Several sub-projects come together in this device
 |_ susi_installer     (Framework which can install all parts on a RPi and Desktops, and also is able to create SUSIbian disk images)
 |_ susi_python        (Python API for the susi_server at https://api.susi.ai or local instance)
 |_ susi_server        (The same server as on api.susi.ai, hosted locally for maximum privacy. No cloud needed)
 |_ susi_skill_data    (The skills as provided by susi_server on api.susi.ai; pulled from the git repository automatically)
 |_ susi_linux         (a state machine in python which uses susi_python, Speech-to-text and Text-to-speech functions)
```

This project provides the following functionality:

- Hotword Detection works for hotword "Susi"
- Voice Detection working with Google Speech API / IBM Watson Speech to Text API.
- Voice Output working with Google TTS / IBM Watson TTS / Flite TTS.
- Susi AI response working through Susi AI [API Python Wrapper](https://github.com/fossasia/susi_python)


## Installation

`susi_linux` is normally installed via the [SUSI Installer](https://github.com/fossasia/susi_installer).
In this case there are binaries for configuration, starting, authentication and
others available in `$HOME/SUSI.AI/bin` (under default installation settings).

In case of manual installations, the wrappers in [`wrapper` directory](wrapper/) need to
be configured to point to the respective installation directories and location of
the `config.json` file.

## Setting up and configuring Susi on Linux / RaspberryPi

Configuration is done via the file [config.json](config.json) which normally
resides in `$HOME/SUSI.AI/config.json`.

If correctly installed, `susi-linux-configure` provides a GUI interface to the configuration
of `susi_linux`, while `susi-linux-config-generator` provides a CLI interface:
```
susi-linux-config-generator <stt> <tts> <hotword_detection> <wake_button>
```
where
- `stt` is the speech to text service, one of the following choices:
    - `google` - use Google STT service
    - `ibm` - IBM/Watson STT
    - `sphinx` - PocketSphinx STT system, working offline
- `tts` is the text to speech service, one of the following choices:
    - `google` - use Google TTS
    - `ibm`  - IBM/Watson TTS (login credential necessary)
    - `flite` - flite TTS service working offline
- `hotword_detection` is the choice if you want to use snowboy detector as the hotword detection or not
    - `y` to use snowboy
    - `n` to use pocket sphinx
- `wake_button` is the choice if you want to use an external wake button or not
    - `y` to use an external wake button
    - `n` to disable the external wake button

Other interfaces for configuration are available for Android and iOS.

Manual configuration is possible, the allowed keys in [`config.json`](config.json) are
- `Device`: the name of the current device
- `WakeButton`: whether a wake button is available or not
- `default_stt`: see above for possible settings
- `default_tts`: see above for possible settings
- `data_base_dir`: directory where support files are installed
- `detection_bell_sound`: sound file that is played when detection starts, relative to `data_base_dir`
- `problem_sound`: sound file that is played on general errors, relative to `data_base_dir`
- `recognition_error_sound`: sound file that is played on detection errors, relative to `data_base_dir`
- `flite_speech_file_path`: flitevox speech file, relative to `data_base_dir`
- `hotword_engine`: see above for possible settings
- `usage_mode`: access mode to `accounts.susi.ai`, either `anonymous` or `authenticated`
- `room_name`: free form description of the room
- `watson_tts_config`: a JSON array with `username` and `password` as keys, providing the credentials for IBM/Watson


For details concerning installation, setup, and operation on RaspberryPi, see
the documentation at [SUSI Installer](https://github.com/fossasia/susi_installer).



## Information for developers

This section is intended for developer.

### **Important:** Tests before making a new release

1. The hotword detection should have a decent accuracy
2. SUSI Linux shouldn't crash when switching from online to offline and vice versa (failing as of now)
3. SUSI Linux should be able to boot offline when no internet connection available (failing as of now)

### Roadmap

- Offline Voice Detection (if possible with satisfactory results)

### General working of SUSI

- SUSI.AI follows a finite state system for the code architecture.
- Google TTS and STT services are used as default services but if the internet fails, a switch to offline services PocketSphinx (STT) and Flite (TTS) is made automatically


### Run SUSI Linux for development purposes

If installed via the SUSI Installer, systemd unit files are installed:
- `ss-susi-linux.service` for the user bus, use as user with `systemctl --user start/enable ss-susi-linux`
- `ss-susi-linux@.service` for the system bus, use as `root` user to start a job for a specific user, 
  independent from whether the user is logged in or not: `sudo systemctl start/enable ss-susi-linux@USER`

By default, it is ran in _production_ mode, where log messages are limited to _error_ and _warning_ only.
In development, you may want to see more logs, to help debugging. You can switch it to "verbose" mode by 2 ways:

1. Run it manually

- Stop systemd service by `sudo systemctl stop ss-susi-linux`
- Use Terminal, _cd_ to `susi_linux` directory and run

```
python3 -m main -v
```
or repeat `v` to increase verbosity:

```
python3 -m main -vv
```

2. Change command run by `systemd`

- Edit the _/lib/systemd/system/ss-susi-linux.service_ and change the command in `ExecStart` parameter:

```ini
ExecStart=/usr/bin/python3 -m main -v --short-log
```
- Reload systemd daemon: `sudo systemctl daemon-reload`
- Restart the servive: `sudo systemctl restart ss-susi-linux`
- Now you can read the log via `journalctl`:

    + `journalctl -u ss-susi-linux`
    + or `journalctl -fu ss-susi-linux` to get updated when the log is continuously produced.

The `-v` option is actually the same as the 1st method. The `--short-log` option is to exclude some info which is already provided by `journalctl`. For more info about `logging` feature, see this GitHub [issue](https://github.com/fossasia/susi_linux/issues/423).

