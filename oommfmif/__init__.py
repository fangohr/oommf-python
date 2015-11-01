import os
import subprocess
import sys


def retrieve_oommf_path():

    # Environment variable OOMMF_PATH should point to the directory which
    # contains 'oommf.tcl'
    if 'OOMMF_PATH' not in os.environ:
        msg = """Please set OOMMF_PATH environment variable to point to
        the directory that contains oommf.tcl. In bash, you can write
        export OOMMF_PATH=/yourhome/youpath/to/oommf

    This can be added to the ~/.bashrc, for example, to be executed
    automatically.

    Cowardly stopping here.
    """

        print(msg)
        sys.exit(1)
    else:
        oommf_path = os.environ['OOMMF_PATH']

    return oommf_path


def retrieve_oommf_executable(path):

    """Given an OOMMF_PATH as path, we either expect 'oommf.tcl' to be the main
    retrieve_oommf_executable or a script called 'oommf' which may call
    oommf.tcl internally, and maybe sets some envinorment     variables. The
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


def call_oommf(argstring, workdir=None):
    """Convenience function to call OOMMF: Typical usage

    p = call_oommf("+version")
    p.wait()
    stdout, stderr = p.stdout.read(), p.stderr.read()

    the 'prefixcommand' allows to execute the command in a different directory.

    """
    if workdir:
        command = "cd {:s} && ".format(workdir)
    else:
        command = ""

    command += os.path.join(oommf_path, oommf_executable) + ' ' + argstring
    print("About to execute: '{}'".format(command))
    p = subprocess.Popen(command,
                         shell=True, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    return p


def get_version():
    """Return OOMMF version as string, something like 1.2.0.5"""
    p = call_oommf('+version')
    p.wait()
    stderr = p.stderr.read()     # version is returned in stderr
    s_oommftcl, versionstring = stderr.split()[0:2]
    return versionstring


def get_oommf_path():
    return oommf_path
