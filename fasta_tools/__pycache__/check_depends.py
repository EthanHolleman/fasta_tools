from shutil import which
import sys
current_dependencies = ['em_cons', 'clustalo']


def check_dependencies():
    '''
    checks for the required software to run methods in the consensus_tools file
    Clustal Omega and Emboss can both be downloaded using sudo apt-get on ubuntu
    '''
    for depend in current_dependencies:
        if which(depend) is None:
            print('This method requires {} to run, please install and then continue'.format(depend))
            sys.exit()
    return False
