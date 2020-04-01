import os
import subprocess
import re
import stat

"""
Change RPATH for openmpi-3.1.4 on chinook, in ALL Spack-compiled binaries
Goes with ~/sh/fixup_openmpi.py
"""

def is_exe(fname):
    return 0 != ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & os.stat(fname)[stat.ST_MODE])


def is_elf(fname):
    with open(fname, "rb") as fin:
        buf = fin.read(4)
        return buf == b'\x7fELF'


#print(is_elf('fixup_chinook.py'))
#print(is_elf('/import/unsupported/TWOWAY/spack/opt/spack/linux-centos6-x86_64/intel-18.5.274/hdf5-1.8.18-35rxhyz2dd4oymkgwo6q42zp5mxcpsjk/lib/libhdf5_fortran.so.10.0.4'))
#print(is_elf('/bin/ls'))
#exit()

#print(is_elf('/import/unsupported/TWOWAY/spack/opt/spack/linux-centos6-x86_64/intel-18.5.274/py-scipy-1.1.0-xlnbbfsqbrjct6lv67y74hvexs4tgkod/lib/python3.5/site-packages/scipy/sparse/_sparsetools.cpython-35m-x86_64-linux-gnu.so'))
#exit()


#CHRPATH = '/import/unsupported/TWOWAY/spack/opt/spack/linux-centos6-x86_64/intel-18.5.274/chrpath-0.16-y6kpfrywjegkg4whsjkx7w3tx6xlehw7/bin/chrpath'
CHRPATH = 'chrpath'       # Or consider using patchelf
chrpathRE = re.compile(r'(.*):\s*(RPATH|RUNPATH)=(.*)')

OLD = '/opt/scyld/openmpi/3.1.4'
#NEW = '/home/eafischer2/bitly/om3.1.4'
NEW = '/home/eafischer2/om3.1.4'

print('xxxx ',__file__)
#dir0 = os.path.abspath(os.path.split(__file__)[0])
#dir1 = os.path.abspath(os.path.join(dir0, '..', '..', '..', '..')
#print('x1 ',dir1)
ROOT = os.path.abspath(os.path.realpath(os.path.join(os.path.split(__file__)[0], '..', '..', '..', '..', 'opt', 'spack')))
print(ROOT)

for root, dirs, files in os.walk(ROOT):
    for file in files:
#        if not (file.startswith('libhdf5')):
#            continue

        fname = os.path.join(root, file)
#        if not '.so' in file:
#            continue
        if os.path.islink(fname):
            continue
#        if not is_exe(fname):
#            continue
        if not is_elf(fname):
            continue
#        print('yy1 ',file)

        try:
            out = subprocess.check_output([CHRPATH, fname]).decode()
#            print('rrrr ', out)
            match = chrpathRE.match(out)
            if match is None:
                continue
            if match is not None:
                RPATH0 = match.group(3)
        except subprocess.CalledProcessError:
            continue    # No RPATH in this file

#        print('RPATH0 ',RPATH0)

        # Transform the rpath
        rpath0 = RPATH0.split(':')
        rpath1 = list()
        for rp0 in rpath0:
            if rp0 == '/usr/lib64':
                continue
            rp1 = rp0.replace(OLD, NEW)

            rpath1.append(rp1)

        RPATH1 = ':'.join(rpath1)
#        print('RPATH1 ', RPATH1)

        if RPATH1 != RPATH0:
            print('---------------- {}'.format(fname))
            if len(RPATH1) != len(RPATH0):
                print('************ len mismatch')
            else:
#                print(RPATH0)
#                print(RPATH1)
                subprocess.run([CHRPATH, '-r', RPATH1, fname])
                print()
