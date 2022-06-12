
## Free Public Servers

Below are the servers you are using for free, it may change along the time. If you are not close to one of these, your network may be slow.
| Location | Vendor | Specification |
| --------- | ------------- | ------------------ |
| Seoul | AWS lightsail | 1 VCPU / 0.5GB RAM |
| Singapore | Vultr | 1 VCPU / 1GB RAM |
| Dallas | Vultr | 1 VCPU / 1GB RAM | |

## Dependencies

Desktop versions use [sciter](https://sciter.com/) for GUI, please download sciter dynamic library yourself.

[Windows](https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.win/x64/sciter.dll) |
[Linux](https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.lnx/x64/libsciter-gtk.so) |
[MacOS](https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.osx/libsciter.dylib)

Mobile versions use Flutter. We will migrate desktop version from Sciter to Flutter.

## Raw steps to build

- Prepare your Rust development env and C++ build env

- Install [vcpkg](https://github.com/microsoft/vcpkg), and set `VCPKG_ROOT` env variable correctly

  - Windows: vcpkg install libvpx:x64-windows-static libyuv:x64-windows-static opus:x64-windows-static
  - Linux/MacOS: vcpkg install libvpx libyuv opus

- run `cargo run`

## [Build]

## How to build on Linux

### Ubuntu 18 (Debian 10)

```sh
sudo apt install -y g++ gcc git curl wget nasm yasm libgtk-3-dev clang libxcb-randr0-dev libxdo-dev libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev cmake
```

### Fedora 28 (CentOS 8)

```sh
sudo yum -y install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libxdo-devel libXfixes-devel pulseaudio-libs-devel cmake alsa-lib-devel
```

### Arch (Manjaro)

```sh
sudo pacman -Syu --needed unzip git cmake gcc curl wget yasm nasm zip make pkg-config clang gtk3 xdotool libxcb libxfixes alsa-lib pulseaudio
```

### Install pynput package

```sh
pip3 install pynput
```

### Install vcpkg

```sh
git clone https://github.com/microsoft/vcpkg
cd vcpkg
git checkout 2021.12.01
cd ..
vcpkg/bootstrap-vcpkg.sh
export VCPKG_ROOT=$HOME/vcpkg
vcpkg/vcpkg install libvpx libyuv opus
```

### Fix libvpx (For Fedora)

```sh
cd vcpkg/buildtrees/libvpx/src
cd *
./configure
sed -i 's/CFLAGS+=-I/CFLAGS+=-fPIC -I/g' Makefile
sed -i 's/CXXFLAGS+=-I/CXXFLAGS+=-fPIC -I/g' Makefile
make
cp libvpx.a $HOME/vcpkg/installed/x64-linux/lib/
cd
```

### Build

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone https://github.com/oliver90129/remoteDesk/kokdesk
cd kokdesk
mkdir -p target/debug
wget https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.lnx/x64/libsciter-gtk.so
mv libsciter-gtk.so target/debug
VCPKG_ROOT=$HOME/vcpkg cargo run
```

### Change Wayland to X11 (Xorg)

KOKDesk does not support Wayland. Check [this](https://docs.fedoraproject.org/en-US/quick-docs/configuring-xorg-as-default-gnome-session/) to configuring Xorg as the default GNOME session.

## How to build with Docker

Begin by cloning the repository and building the docker container:

```sh
git clone https://github.com/oliver90129/remoteDesk/kokdesk
cd kokdesk
docker build -t "kokdesk-builder" .
```

Then, each time you need to build the application, run the following command:

```sh
docker run --rm -it -v $PWD:/home/user/kokdesk -v kokdesk-git-cache:/home/user/.cargo/git -v kokdesk-registry-cache:/home/user/.cargo/registry -e PUID="$(id -u)" -e PGID="$(id -g)" kokdesk-builder
```

Note that the first build may take longer before dependencies are cached, subsequent builds will be faster. Additionally, if you need to specify different arguments to the build command, you may do so at the end of the command in the `<OPTIONAL-ARGS>` position. For instance, if you wanted to build an optimized release version, you would run the command above followed by `--release`. The resulting executable will be available in the target folder on your system, and can be run with:

```sh
target/debug/kokdesk
```

Or, if you're running a release executable:

```sh
target/release/kokdesk
```

Please ensure that you are running these commands from the root of the KOKDesk repository, otherwise the application may be unable to find the required resources. Also note that other cargo subcommands such as `install` or `run` are not currently supported via this method as they would install or run the program inside the container instead of the host.

## File Structure

- **[libs/hbb_common]: video codec, config, tcp/udp wrapper, protobuf, fs functions for file transfer, and some other utility functions
- **[libs/scrap]: screen capture
- **[libs/enigo]: platform specific keyboard/mouse control
- **[src/ui]: GUI
- **[src/server]: audio/clipboard/input/video services, and network connections
- **[src/client.rs]: start a peer connection
- **[src/rendezvous_mediator.rs]: Communicate with [kokdesk-server], wait for remote direct (TCP hole punching) or relayed connection
- **[src/platform]: platform specific code
- **[flutter]: Flutter code for mobile
- **[flutter/web/js]: Javascript for Flutter web client


