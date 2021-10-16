#!/usr/bin/env bash

set -e

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

VERSION="master"
DIR="p"
NAME="yaml-cpp"
GIT_URL="https://github.com/jbeder/${NAME}"

HAS=1
[ ! -d "$CWD/$DIR" ] && HAS=0 && git clone --depth 1 $GIT_URL -b $VERSION $DIR --recursive

[ $HAS -eq 1 ] && git pull --recurse-submodules origin $VERSION

cp dll.h ${DIR}/include/${NAME}

exit 0
