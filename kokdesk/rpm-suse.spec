Name:       kokdesk 
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 pulseaudio-utils alsa-utils arphic-uming-fonts python3-pip curl libXtst6 python3-devel

%description
The best open-source remote desktop client software, written in Rust. 

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/kokdesk/
mkdir -p %{buildroot}/usr/share/kokdesk/files/
install -m 755 $HBB/target/release/kokdesk %{buildroot}/usr/bin/kokdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/lib/kokdesk/libsciter-gtk.so
install $HBB/kokdesk.service %{buildroot}/usr/share/kokdesk/files/
install $HBB/256-no-margin.png %{buildroot}/usr/share/kokdesk/files/kokdesk.png
install $HBB/kokdesk.desktop %{buildroot}/usr/share/kokdesk/files/
install $HBB/pynput_service.py %{buildroot}/usr/share/kokdesk/files/

%files
/usr/bin/kokdesk
/usr/lib/kokdesk/libsciter-gtk.so
/usr/share/kokdesk/files/kokdesk.service
/usr/share/kokdesk/files/kokdesk.png
/usr/share/kokdesk/files/kokdesk.desktop
/usr/share/kokdesk/files/pynput_service.py

%changelog
# let's skip this for now

# https://www.cnblogs.com/xingmuxin/p/8990255.html
%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    service kokdesk stop || true
  ;;
esac

%post
cp /usr/share/kokdesk/files/kokdesk.service /etc/systemd/system/kokdesk.service
cp /usr/share/kokdesk/files/kokdesk.desktop /usr/share/applications/
sudo -H pip3 install pynput
systemctl daemon-reload
systemctl enable kokdesk
systemctl start kokdesk
update-desktop-database

%preun
systemctl stop kokdesk || true
systemctl disable kokdesk || true
rm /etc/systemd/system/kokdesk.service || true

%postun
rm /usr/share/applications/kokdesk.desktop || true
update-desktop-database
