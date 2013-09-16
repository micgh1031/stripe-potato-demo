#!/usr/bin/env python

import os
import subprocess

venv = os.environ.get('VIRTUAL_ENV', None)

if venv is None:
    print 'You need create a virtualenv first'
    exit(1)

print 'Installing Fabric..'
ret = subprocess.call('%s/bin/pip install fabric' % venv, shell=True)

if ret:
    print 'Sorry something went wrong. you may need to install Fabric manually?'
else:
    print 'Done. You can now use the Fabric commands.'
