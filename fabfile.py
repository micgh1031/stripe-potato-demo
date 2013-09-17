#/usr/bin/env python2.7
import os
import sys

from fabric.api import env, task
from fabric.operations import local
from fabric.context_managers import lcd


BASEDIR = os.path.dirname(__file__)

env.hosts = ['localhost']

APP_DIR = os.path.join(BASEDIR, "app")

REQUIREMENTS = "requirements.txt"
REQUIREMENTS_DEV = "requirements-dev.txt"

bin_dir = 'bin' if not sys.platform == 'win32' else 'Scripts'  # Yes, virtualenv on win32 _is_ that stupid


def get_venv():
    """ Get the current virtual environment name
        and bail if we're not in one
    """
    try:
        return os.environ['VIRTUAL_ENV']
    except KeyError:
        print 'Not in a virtualenv'
        exit(1)


def get_pip():
    """ Get an absolute path to the pip executable
        for the current virtual environment
    """
    return os.path.join(get_venv(), bin_dir, 'pip')


def get_python():
    """ Get an absolute path to the python executable
        for the current virtual environment
    """
    return os.path.join(get_venv(), bin_dir, 'python')


@task
def remove_pyc():
    local("find . -name '*.pyc' -delete")


@task(alias="local_deps")
def install_dev_dependencies():
    """ Install the development only deps
    """
    with lcd(BASEDIR):
        cmd = '%(pip)s install -r %(requirements_file)s' % {
            'pip': get_pip(),
            'requirements_file': REQUIREMENTS_DEV
        }
        local(cmd)


@task(alias="deps")
def install_deployable_dependencies():
    """ Install the deployable dependencies
    """
    with lcd(BASEDIR):
        cmd = '%(pip)s install -U --force-reinstall -r %(requirements_file)s' % {
            'pip': get_pip(),
            'requirements_file': REQUIREMENTS
        }
        local(cmd)

@task
def runserver():
    """"""
    python = get_python()
    manage_py = os.path.join(APP_DIR, 'manage.py')
    os.execvp(python, [python, manage_py, 'runserver'])
