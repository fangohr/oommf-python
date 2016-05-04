"""
oommfmif: A module for calling OOMMF from Python.

"""
import os
import subprocess
import sys
from textwrap import dedent


def retrieve_oommf_path():
    """
    retrieve_oommf_path()
    Gets value from the environment variable oommf_path.

    Returns
    -------
    string
        Path to folder containing oommf.tcl
    Notes
    -----
    Environment variable OOMMF_PATH should point to the directory which
    contains 'oommf.tcl'
    """
    if 'OOMMF_PATH' not in os.environ:
        msg = dedent("""\
            Please set the OOMMF_PATH environment variable to point to the
            directory that contains the file 'oommf.tcl'. In bash, you can
            write:

                export OOMMF_PATH=/yourhome/yourpath/to/oommf

            This can be added to the ~/.bashrc, for example, to be executed
            automatically.

            Cowardly stopping here.
            """)

        print(msg)
        sys.exit(1)
    else:
        oommf_path = os.environ['OOMMF_PATH']
    return oommf_path


def retrieve_oommf_executable(path):
    """Given an OOMMF_PATH as path, we either expect 'oommf.tcl' to be the main
    retrieve_oommf_executable or a script called 'oommf' which may call
    oommf.tcl internally, and maybe sets some envinorment variables. The
    conda oommf installation creates such a 'oommf' shell script."""

    oommf_path = path
    files = os.listdir(oommf_path)
    if 'oommf' in files and 'oommf.tcl' not in files:
        return 'oommf'
    elif 'oommf.tcl' in files and 'oommf' not in files:
        return 'oommf.tcl'
    elif 'oommf' in files and 'oommf.tcl' in files:
        msg = "There is 'oommf' and 'oommf.tcl' in {}. Don't now which"\
            " one to use".format(oommf_path)
        print(msg)
        raise RuntimeError(msg)
    elif 'oommf' not in files and 'oommf.tcl' not in files:
        msg = "Can't find 'oommf' or 'oommf.tcl' in {}. Giving up."\
            .format(oommf_path)
        print(msg)
        raise RuntimeError(msg)
    else:
        msg = "Unknown outcome - shoudn't be possible."
        raise NotImplementedError(msg)


oommf_path = retrieve_oommf_path()
oommf_executable = retrieve_oommf_executable(oommf_path)


def call_oommf(argstring, workdir=None, print_output=True):
    """Convenience function to call OOMMF: Typical usage

    p = call_oommf("+version")
    p.wait()
    stdout, stderr = p.stdout.read(), p.stderr.read()

    the 'prefixcommand' allows to execute the command in a different directory.

    """
    if workdir:
        command = "cd {} && ".format(workdir)
    else:
        command = ""

    command += os.path.join(oommf_path, oommf_executable) + ' ' + argstring
    print("About to execute: '{}'".format(command))
    p = subprocess.Popen(command,
                         shell=True, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE, universal_newlines=True)

    return p


def get_version():
    """Return OOMMF version as string, something like 1.2.0.5"""
    p = call_oommf('+version')
    p.wait()
    stderr = p.stderr.readlines()     # version is returned in stderr
    # output is something like  "<15330> oommf.tcl 1.2.0.6  info:\noommf.tcl
    # 1.2.0.6"
    line = stderr[0].decode()
    assert 'oommf.tcl' in line
    versionstring = line.split('oommf.tcl')[1].strip()
    return versionstring


def get_oommf_path():
    return oommf_path
