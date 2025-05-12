#!/bin/sh
dpkg-buildpackage -us -uc
rm -rf build
mkdir -p build
mv ../pdfsuite_*.tar.gz ../pdfsuite_*.dsc ../pdfsuite_*_all.deb ../pdfsuite_*_amd64.buildinfo ../pdfsuite_*_amd64.changes build
