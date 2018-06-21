#!/bin/sh

set -ev

VERSION=`cat VERSION.txt`

docker build -t trinityctat/scellismb2018:$VERSION .
docker build -t trinityctat/scellismb2018:latest .

