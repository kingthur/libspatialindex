#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

pkgname = 'libspatialindex'
pkgdir = 'python'

init_py = """\
def get_dir():
    import os
    return os.path.dirname(__file__)
"""


def bootstrap():
    import distutils
    import os
    distutils.dir_util.mkpath(pkgdir)
    with open(os.path.join(pkgdir, '__init__.py'), 'w') as f:
        f.write(init_py)


class install(_install):
    def run(self):
        from os import path
        import subprocess

        prefix = path.join(path.abspath(self.install_platlib), pkgname)
        subprocess.check_call(["./autogen.sh"])
        subprocess.check_call(["./configure", "--prefix=" + prefix,
                               "--enable-shared", "--disable-static"])
        subprocess.check_call(["make"])
        subprocess.check_call(["make", "install"])
        _install.run(self)


def version():
    import re
    matcher = re.compile(r'#define\s+SIDX_RELEASE_NAME\s+\"(.*)\"')
    with open('include/spatialindex/Version.h', 'r') as f:
        result, = matcher.search(f.read()).groups()
        return result

bootstrap()
setup(name=pkgname,
      version=version(),
      packages=[pkgname],
      package_dir={pkgname: pkgdir},
      cmdclass={'install': install},
      zip_safe=False)
