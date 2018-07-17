#!/usr/bin/env python3
"""Clean old snap revision on Ubuntu

This script removes all old snap revisions.
It needs 'sudo' to run 'snap remove'.
"""

import os
import sys

def get_using_version():
    snaps = {}
    snapslines = os.popen('snap list').readlines()[1:]
    for line in snapslines:
        infos = line.split()
        snaps[infos[0]] = infos[2]
    return snaps

def get_all_version():
    snaps = {}
    snaplines = os.popen('df').readlines()[1:]
    for line in snaplines:
        if '/snap/' in line:
            infos = line.split()[5].split('/')
            if infos[2] in snaps:
                snaps[infos[2]].append(infos[3])
            else:
                snaps[infos[2]] = [infos[3]]
    return snaps

def get_old_version():
    using_ver = get_using_version()
    all_ver = get_all_version()
    old_ver = {}
    for k, v in using_ver.items():
        old_ver[k] = [i for i in all_ver[k] if i != v]
    return old_ver

def main():
    olds = get_old_version()
    tip_flag = False
    for k, v in olds.items():
        for old in v:
            print('removing snap package %s: (revision: %s)...' % (k, old))
            os.system('sudo snap remove %s --revision %s' % (k, old))
            tip_flag = True
    if tip_flag:
        print('remove old versions finished.')
    else:
        print('no old snap version.')

if __name__ == "__main__":
    sys.exit(main())