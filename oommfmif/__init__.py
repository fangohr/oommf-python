import os
import subprocess

# Environment variable OOMMF_PATH should point to the directory which
# contains 'oommf.tcl'
oommf_path = os.environ['OOMMF_PATH']


def call_oommf(argstring):
    """Convenience function to call OOMMF: Typicallusage

    p = call_oommf("+version")
    p.wait()
    stdout, stderr = p.stdout.read(), p.stderr.read()

    """

    p = subprocess.Popen(os.path.join(oommf_path, 'oommf.tcl') +
                         ' ' + argstring,
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
