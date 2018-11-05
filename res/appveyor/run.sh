#!/usr/bin/env bash

set -ex

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CWD/../..
ROOT=$PWD

export MKN_CL_PREFERRED=1
export PYTHON=/c/Python36-x64/python.exe
mkn clean build -dtSOg 0
$PYTHON /c/Python36-x64/Scripts/flawfinder .
rm -rf bin/build/tmp bin/build/obj
mkdir -p win/master
cp bin/build/* win/master
tar cf mkn.tar win