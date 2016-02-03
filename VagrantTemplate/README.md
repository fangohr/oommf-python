# Vagrant Template

This template can be used with Vagrant in order to set up a fully configured Ubuntu Virtual Machine which has a working installation of OOMMF, and JOOMMF.

To use, install vagrant and VirtualBox and then from this folder type:

    vagrant up
    #This will take a while, as it builds OOMMF from scratch.
    vagrant ssh -- -X

and you will then be logged into the virtual machine. To use OOMMF or JOOMMF, type either 'oommf' or from inside Python
    import pyoommf
    
