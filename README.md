# Susi Linux

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/167b701c744841c5a05269d06b863732)](https://app.codacy.com/app/fossasia/susi_linux?utm_source=github.com&utm_medium=referral&utm_content=fossasia/susi_linux&utm_campaign=badger)
[![Build Status](https://travis-ci.org/fossasia/susi_linux.svg?branch=master)](https://travis-ci.org/fossasia/susi_linux)
[![Join the chat at https://gitter.im/fossasia/susi_hardware](https://badges.gitter.im/fossasia/susi_hardware.svg)](https://gitter.im/fossasia/susi_hardware?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Dependency Status](https://beta.gemnasium.com/badges/github.com/fossasia/susi_linux.svg)](https://beta.gemnasium.com/projects/github.com/fossasia/susi_linux)

SUSI AI on Linux

This project aims at creating an implementation of Susi, capable to run on Linux
computers and Linux devices in headless mode. It will enable you to bring Susi AI
intelligence to all computers and devices you may think like a Speaker, Car etc.

This project provides the following functionality:

- Voice Detection working with Google Speech API / IBM Watson Speech to Text API.
- Voice Output working with Google TTS / IBM Watson TTS / Flite TTS.
- Susi AI response working through Susi AI [API Python Wrapper](https://github.com/fossasia/susi_python)
- Hotword Detection works for hotword "Susi"
- Audio parsing working through SOX
- Youtube audio working MPV player

## **Important:** Tests before making a new release

1. The hotword detection should have a decent accuracy
2. SUSI Linux shouldn't crash when switching from online to offline and vice versa (failing as of now)
3. SUSI Linux should be able to boot offline when no internet connection available (failing as of now)

### Roadmap

- Offline Voice Detection (if possible with satisfactory results)

### General working of SUSI

- SUSI.AI follows a finite state system for the code architecture.
- Google TTS and STT services are used as default services but if the internet fails, a switch to offline services PocketSphinx (STT) and Flite (TTS) is made automatically


## Setting up and configuring Susi on Linux / RaspberryPi

See the documentation at [SUSI Installer](https://github.com/fossasia/susi_installer).


## Run SUSI Linux for development purposes

This section is intended for developer.

SUSI Linux application is run automatically by `systemd`. The main component is run as _ss-susi-linux.service_. By default, it is ran in _production_ mode, where log messages are limited to _error_ and _warning_ only. In development, you may want to see more logs, to help debugging. You can switch it to "verbose" mode by 2 ways:

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

