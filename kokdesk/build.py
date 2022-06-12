#!/usr/bin/env python3

import os
import platform
import zlib
from shutil import copy2
import hashlib

windows = platform.platform().startswith('Windows')
osx = platform.platform().startswith('Darwin') or platform.platform().startswith("macOS")
hbb_name = 'kokdesk' + ('.exe' if windows else '')
exe_path = 'target/release/' + hbb_name


def get_version():
    with open("Cargo.toml") as fh:
        for line in fh:
            if line.startswith("version"):
                return line.replace("version", "").replace("=", "").replace('"', '').strip()
    return ''


def main():
    os.system("cp Cargo.toml Cargo.toml.bk")
    os.system("cp src/main.rs src/main.rs.bk")
    if windows:
        txt = open('src/main.rs', encoding='utf8').read()
        with open('src/main.rs', 'wt', encoding='utf8') as fh:
            fh.write(txt.replace(
                '//#![windows_subsystem', '#![windows_subsystem'))
    if os.path.exists(exe_path):
        os.unlink(exe_path)
    os.system('python3 inline-sciter.py')
    if os.path.isfile('/usr/bin/pacman'):
        os.system('git checkout src/ui/common.tis')
    version = get_version()
    if windows:
        os.system('cargo build --release --features inline')
        # os.system('upx.exe target/release/kokdesk.exe')
        os.system('mv target/release/kokdesk.exe target/release/KOKDesk.exe')
        pa = os.environ.get('P')
        if pa:
          os.system('signtool sign /a /v /p %s /debug /f .\\cert.pfx /t http://timestamp.digicert.com  target\\release\\kokdesk.exe'%pa)
        else:
          print('Not signed')
        os.system('cp -rf target/release/KOKDesk.exe kokdesk-%s-putes.exe'%version)
    elif os.path.isfile('/usr/bin/pacman'):
        os.system('cargo build --release --features inline')
        os.system('git checkout src/ui/common.tis')
        os.system('strip target/release/kokdesk')
        os.system("sed -i 's/pkgver=.*/pkgver=%s/g' PKGBUILD"%version)
        # pacman -S -needed base-devel
        os.system('HBB=`pwd` makepkg -f')
        os.system('mv kokdesk-%s-0-x86_64.pkg.tar.zst kokdesk-%s-manjaro-arch.pkg.tar.zst'%(version, version))
        # pacman -U ./kokdesk.pkg.tar.zst
    elif os.path.isfile('/usr/bin/yum'):
        os.system('cargo build --release --features inline')
        os.system('strip target/release/kokdesk')
        os.system("sed -i 's/Version:    .*/Version:    %s/g' rpm.spec"%version)
        os.system('HBB=`pwd` rpmbuild -ba rpm.spec')
        os.system('mv $HOME/rpmbuild/RPMS/x86_64/kokdesk-%s-0.x86_64.rpm ./kokdesk-%s-fedora28-centos8.rpm'%(version, version))
        # yum localinstall kokdesk.rpm
    elif os.path.isfile('/usr/bin/zypper'):
        os.system('cargo build --release --features inline')
        os.system('strip target/release/kokdesk')
        os.system("sed -i 's/Version:    .*/Version:    %s/g' rpm-suse.spec"%version)
        os.system('HBB=`pwd` rpmbuild -ba rpm-suse.spec')
        os.system('mv $HOME/rpmbuild/RPMS/x86_64/kokdesk-%s-0.x86_64.rpm ./kokdesk-%s-suse.rpm'%(version, version))
        # yum localinstall kokdesk.rpm

    else:
        os.system('cargo bundle --release --features inline')
        if osx:
            os.system(
                'strip target/release/bundle/osx/KOKDesk.app/Contents/MacOS/kokdesk')
            os.system(
                'cp libsciter.dylib target/release/bundle/osx/KOKDesk.app/Contents/MacOS/')
            # https://github.com/sindresorhus/create-dmg
            os.system('/bin/rm -rf *.dmg')
            plist = "target/release/bundle/osx/KOKDesk.app/Contents/Info.plist"
            txt = open(plist).read()
            with open(plist, "wt") as fh:
                fh.write(txt.replace("</dict>", """
  <key>LSUIElement</key>    
  <string>1</string>    
</dict>"""))
            pa = os.environ.get('P')
            if pa:
              os.system('''
# buggy: rcodesign sign ... path/*, have to sign one by one
#rcodesign sign --p12-file ~/.p12/kokdesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./target/release/bundle/osx/KOKDesk.app/Contents/MacOS/kokdesk
#rcodesign sign --p12-file ~/.p12/kokdesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./target/release/bundle/osx/KOKDesk.app/Contents/MacOS/libsciter.dylib
#rcodesign sign --p12-file ~/.p12/kokdesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./target/release/bundle/osx/KOKDesk.app
# goto "Keychain Access" -> "My Certificates" for below id which starts with "Developer ID Application:"
codesign -s "Developer ID Application: {0}" --force --options runtime  ./target/release/bundle/osx/KOKDesk.app/Contents/MacOS/*
codesign -s "Developer ID Application: {0}" --force --options runtime  ./target/release/bundle/osx/KOKDesk.app
'''.format(pa))
            os.system('create-dmg target/release/bundle/osx/KOKDesk.app')
            os.rename('KOKDesk %s.dmg'%version, 'kokdesk-%s.dmg'%version)
            if pa:
              os.system('''
#rcodesign sign --p12-file ~/.p12/kokdesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./kokdesk-{1}.dmg
codesign -s "Developer ID Application: {0}" --force --options runtime ./kokdesk-{1}.dmg
# https://pyoxidizer.readthedocs.io/en/latest/apple_codesign_rcodesign.html
rcodesign notarize --api-issuer 69a6de7d-2907-47e3-e053-5b8c7c11a4d1 --api-key 9JBRHG3JHT --staple ./kokdesk-{1}.dmg
# verify:  spctl -a -t exec -v /Applications/KOKDesk.app
'''.format(pa, version))
            else:
              print('Not signed')
        else:
            os.system('mv target/release/bundle/deb/kokdesk*.deb ./kokdesk.deb')
            os.system('dpkg-deb -R kokdesk.deb tmpdeb')
            os.system('mkdir -p tmpdeb/usr/share/kokdesk/files/systemd/')
            os.system(
                'cp kokdesk.service tmpdeb/usr/share/kokdesk/files/systemd/')
            os.system('cp pynput_service.py tmpdeb/usr/share/kokdesk/files/')
            os.system('cp DEBIAN/* tmpdeb/DEBIAN/')
            os.system('strip tmpdeb/usr/bin/kokdesk')
            os.system('mkdir -p tmpdeb/usr/lib/kokdesk')
            os.system('cp libsciter-gtk.so tmpdeb/usr/lib/kokdesk/')
            md5_file('usr/share/kokdesk/files/systemd/kokdesk.service')
            md5_file('usr/share/kokdesk/files/pynput_service.py')
            md5_file('usr/lib/kokdesk/libsciter-gtk.so')
            os.system('dpkg-deb -b tmpdeb kokdesk.deb; /bin/rm -rf tmpdeb/')
            os.rename('kokdesk.deb', 'kokdesk-%s.deb'%version)
    os.system("mv Cargo.toml.bk Cargo.toml")
    os.system("mv src/main.rs.bk src/main.rs")


def md5_file(fn):
    md5 = hashlib.md5(open('tmpdeb/' + fn, 'rb').read()).hexdigest()
    os.system('echo "%s %s" >> tmpdeb/DEBIAN/md5sums' % (md5, fn))


if __name__ == "__main__":
    main()
