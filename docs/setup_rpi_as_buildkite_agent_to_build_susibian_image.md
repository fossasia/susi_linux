# Setup RPi as Buildkite agent to build SUSIbian image

## 1. Install software

- The RPi should be flashed with Raspbian Lite. The ReSpeaker driver must not be installed.
- Install `apt-cacher-ng` (with `apt`). This is to cache _deb_ packages, help reduce build time.
- Rename your RPi hostname (_/etc/hostname_, _/etc/hosts_) to not clash with the existing agents in https://buildkite.com/organizations/fossasia/agents.
- Install `buildkite-agent`, following Buildkite [documentation](https://buildkite.com/docs/agent/v3/debian).
- Install some tools as listed in https://github.com/fossasia/pi-gen#dependencies

## 2. Configuration
- Let `apt-cacher-ng` start automatically on boot: `sudo systemctl enable apt-cacher-ng`
- Set token for `buildkite-agent`, it can be grabbed [here](https://buildkite.com/organizations/fossasia/agents#setup-debian).
- Generate SSH key for `buildkite-agent` user. Note that the home directory of this user is `/var/lib/buildkite-agent`. You can do it by:

```
sudo su buildkite-agent
ssh-keygen -t ed25519
exit
```

Here, we use `sudo su` instead of `su`, to type our password, instead of `buildkite-agent`'s password (which doesn't exist). For SSH key type, `Ed25519` is just my personal preference (which is new, fast, short key length), you can use the more common type RSA.

- Add SSH host for the hosting server (the server which the build script will upload image to), by adding these lines to `/var/lib/buildkite-agent/.ssh/config`

```
Host img-storage
    User <remote_user>
    Hostname <server_ip>
```
- You must try this SSH configuration, to make sure it works, and to let SSH accept server's fingerprint.
- Make `buildkite-agent` user have `sudo` permission (`sudo adduser buildkite-agent sudo`) and not require password to execute `sudo`, by adding file _/etc/sudoers.d/buildkite-agent_ with this content:

```
buildkite-agent ALL=(ALL) NOPASSWD: ALL
```
- Don't forget to let `buildkite-agent` start up automatically.
- Reboot RPI after finishing configuration.
