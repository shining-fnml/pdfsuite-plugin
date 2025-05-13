#!/bin/sh
dpkg-buildpackage -us -uc
rm -rf build
mkdir -p build
mv ../pdfsuite*.tar.gz ../pdfsuite*.dsc ../pdfsuite*_all.deb ../pdfsuite*_amd64.buildinfo ../pdfsuite*_amd64.changes build
