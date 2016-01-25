#!/bin/bash

sudo apt-get update                                                                                                                    │==> default: Building dependency tree...
sudo apt-get upgrade                                                                                                                   │==> default: Reading state information...
#sudo apt-get install build-essential, python, git                                                                                     │==> default: The following packages have been kept back:
sudo apt-get install tcl, tk, tcl8.6-dev, tk8.6-dev                                                                                   │==> default:   linux-headers-generic linux-headers-virtual linux-image-virtual
git clone https://github.com/fangohr/oommf.git                                                                                         │==> default:   linux-virtual
git clone https://github.com/fangohr/oommf-python.git                                                                                  │==> default: The following packages will be upgraded:
cd oommf                                                                                                                              │==> default:   bind9-host cloud-init coreutils dnsutils gcc-4.9-base grub-common grub-pc
make
