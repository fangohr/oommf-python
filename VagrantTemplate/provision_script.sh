#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y --force-yes build-essential
sudo apt-get install -y --force-yes git 
sudo apt-get install -y --force-yes tcl tk tcl8.6-dev tk8.6-dev
git clone https://github.com/fangohr/oommf.git 
git clone https://github.com/fangohr/oommf-python.git
cd oommf 
export OOMMF_TK_CONFIG=/usr/lib/x86_64-linux-gnu/tk8.6/tkConfig.sh
export OOMMF_TCL_CONFIG=/usr/lib/x86_64-linux-gnu/tcl8.6/tclConfig.sh
make
