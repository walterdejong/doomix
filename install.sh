#! /bin/bash
#
#   DOOMix install.sh
#

DESTDIR=${DESTDIR:-/usr}

if [ ! -e doomix.py ]
then
    echo "error: DOOMix source files not found"
    echo "please chdir to source directory"
    exit 1
fi

#apt-get install python3-pyqt5

install -o root -g root -m 755 doomix.py $DESTDIR/games/doomix
install -o root -g root -m 644 -D doomix_icon.png $DESTDIR/share/doomix/doomix_icon.png
install -o root -g root -m 644 -D doomix_logo.png $DESTDIR/share/doomix/doomix_logo.png
install -o root -g root -m 644 -D skull_icon.png $DESTDIR/share/doomix/skull_icon.png
install -o root -g root -m 644 -D doomix.desktop $DESTDIR/share/applications/doomix.desktop
install -o root -g root -m 644 -D README.md $DESTDIR/share/doc/doomix/README.md
install -o root -g root -m 644 -D LICENSE.txt $DESTDIR/share/doc/doomix/LICENSE.txt

# EOB
