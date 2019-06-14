from shutil import which
import sys
current_dependencies = ['em_cons', 'clustalo']


def check_dependencies():
    for depend in current_dependencies:
        if which(depend) is None:
            print('This method requires {} to run, please install and then continue'.format(depend))
            sys.exit()
    return False
