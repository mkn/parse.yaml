

@ECHO off
SET PWD=%CD%
SET VERSION="master"
SET URL="https://github.com/jbeder/yaml-cpp"

IF NOT EXIST %PWD%\p (
git clone --depth 5 %URL% -b %VERSION% p --recursive || exit 666 /b
cp dll.h p\include\yaml-cpp\dll.h
)
