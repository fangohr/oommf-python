#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y --force-yes build-essential
sudo apt-get install -y --force-yes git 
sudo apt-get install -y --force-yes tcl tk tcl8.6-dev tk8.6-dev
sudo apt-get install -y --force-yes python-pip
sudo pip install pytest
git clone https://github.com/fangohr/oommf.git 
git clone https://github.com/fangohr/oommf-python.git
cd oommf 
export OOMMF_TK_CONFIG=/usr/lib/x86_64-linux-gnu/tk8.6/tkConfig.sh
export OOMMF_TCL_CONFIG=/usr/lib/x86_64-linux-gnu/tcl8.6/tclConfig.sh
echo "export OOMMF_TK_CONFIG=/usr/lib/x86_64-linux-gnu/tk8.6/tkConfig.sh" >> /home/vagrant/.bashrc
echo "export OOMMF_TCL_CONFIG=/usr/lib/x86_64-linux-gnu/tcl8.6/tclConfig.sh" >> /home/vagrant/.bashrc
echo "alias oommf=\"tclsh /home/vagrant/oommf/oommf/oommf.tcl\"" >> /home/vagrant/.bashrc
echo "export OOMMF_PATH=/home/vagrant/oommf/oommf/" >> /home/vagrant/.bashrc
echo "export PYTHONPATH=\${PYTHONPATH}:/home/vagrant/oommf-python/" >> /home/vagrant/.bashrc

pwd
make
