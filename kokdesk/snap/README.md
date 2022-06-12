## How to build and run with Snap

Begin by cloning the repository and make sure snapcraft is installed in your Linux.

```sh
# if snapcraft is installed, please skip this
sudo snap install snapcraft --classic
# build kokdesk snap package
snapcraft --use-lxd
# install kokdesk snap package, `--dangerous` flag must exists if u manually build and install kokdesk
sudo snap install kokdesk_xxx.snap --dangerous
```

Note: Some of interfaces needed by KOKDesk cannot automatically connected by Snap. Please **manually** connect them by executing:
```sh
# record system audio
snap connect kokdesk:audio-record
snap connect kokdesk:pulseaudio
# observe loginctl session
snap connect kokdesk:login-session-observe
```

After steps above, KOKDesk can be found in System App Menu.

