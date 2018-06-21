#!/bin/sh

set -ev

VERSION=`cat VERSION.txt`

docker push trinityctat/scellismb2018:${VERSION}
docker push trinityctat/scellismb2018:latest
