#!/bin/bash

APP_ID=org.flozz.calcleaner
APP_NAME=calcleaner

# Print usage and exit if we have not arguments
if [ -z "$1" ] ; then
    echo "USAGE:"
    echo "  ./copy-data.sh <PREFIX>"
    echo
    echo "EXAMPLE:"
    echo "  ./copy-data.sh /usr"
    exit 1
fi

PREFIX=$(realpath $1)

# Go to the script directory
cd "${0%/*}" 1> /dev/null 2> /dev/null

# Copy desktop file
mkdir -pv "$PREFIX/share/applications/"
cp -v "./$APP_ID.desktop" "$PREFIX/share/applications/"

# Copy icons
for size in 32 64 128 256 ; do
    mkdir -pv "$PREFIX/share/icons/hicolor/${size}x${size}/apps/"
    cp -v "../$APP_NAME/data/images/${APP_NAME}_${size}.png" \
          "$PREFIX/share/icons/hicolor/${size}x${size}/apps/$APP_ID.png"
done
mkdir -pv "$PREFIX/share/icons/hicolor/scalable/apps/"
cp -v "../$APP_NAME/data/images/${APP_NAME}.svg" \
      "$PREFIX/share/icons/hicolor/scalable/apps/$APP_ID.svg"

# Update icon cache for real installation
if [ "$PREFIX" == "/usr" ] ; then
    update-icon-caches /usr/share/icons/*
fi

# Copy man page
mkdir -pv "$PREFIX/share/man/man1/"
cp -v "./$APP_NAME.1" "$PREFIX/share/man/man1/$APP_NAME.1"
sed -i "s/{VERSION}/$(python3 ../setup.py --version)/g" "$PREFIX/share/man/man1/$APP_NAME.1"

# Copy the Appstream file
mkdir -pv "$PREFIX/share/metainfo/"
cp -v "./$APP_ID.metainfo.xml" "$PREFIX/share/metainfo/$APP_ID.metainfo.xml"
