#!/bin/bash

set -ev

wget https://download2.rstudio.org/rstudio-server-1.0.153-amd64.deb

gdebi -n rstudio-server-1.0.153-amd64.deb

echo "server-app-armor-enabled=0" >> /etc/rstudio/rserver.conf

