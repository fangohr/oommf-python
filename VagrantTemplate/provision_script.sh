#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y build-essential
sudo apt-get install -y git -y  
sudo apt-get install -y tcl tk tcl8.6-dev tk8.6-dev
git clone https://github.com/fangohr/oommf.git 
git clone https://github.com/fangohr/oommf-python.git
cd oommf 
make
