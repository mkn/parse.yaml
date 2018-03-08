#!/usr/bin/env bash

set -e

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

VERSION="master"
DIR="p"
GIT_URL="https://github.com/jbeder/yaml-cpp"

HAS=1
[ ! -d "$CWD/$DIR" ] && HAS=0 && git clone --depth 1 $GIT_URL -b $VERSION $DIR --recursive

[ $HAS -eq 1 ] && git pull --recurse-submodules origin $VERSION
