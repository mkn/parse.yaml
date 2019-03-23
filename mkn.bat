

@ECHO off
SET PWD=%CD%
SET VERSION="master"
SET URL="https://github.com/jbeder/yaml-cpp"

IF NOT EXIST %PWD%\p (
git clone --depth 1 %URL% -b %VERSION% p --recursive || exit 666 /b
)
cd %PWD%\p
rem issue in yaml-cpp
git reset HEAD~1 --hard

