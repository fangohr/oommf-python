import subprocess


def get_version():
    p = subprocess.Popen("~/git/oommf/oommf/oommf.tcl +version", shell=True,
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.stdout.read(), p.stderr.read()

    # version is returned in stderr
    print(stderr.split()[0:2])
    s_oommftcl, versionstring = stderr.split()[0:2]
    return versionstring
