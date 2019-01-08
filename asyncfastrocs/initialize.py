#!/usr/bin/env python

import sys, os
from asyncfastrocs import version

def main(argv):
    _dir, name = os.path.split(__file__)
    command = f'cp -av {_dir}/config.py {_dir}/qserver.sql .'
    print(command)
    os.system(command)

    command = f'rm -rf instance'
    print(command)
    os.system(command)

    command = f'mkdir instance'
    print(command)
    os.system(command)

    command = f'sqlite3 instance/qserver.db < qserver.sql'
    print(command)
    os.system(command)

    ver = version.ASYNCFASTROCS_VERSION
    command = f'cp -av {_dir}/../asyncfastrocs-{ver}.dist-info/METADATA .'
    print(command)
    os.system(command)

if __name__ == '__main__':
    main(sys.argv)
