from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'fasta_tools', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='fasta_tools',
    version=version['__version__'],
    description=('Some basic fasta methods I use'),
    long_description=long_description,
    author='Ethan Holleman',
    author_email='bruce.wayne@example.com',
    url='https://github.com/ethanholleman/fasta_tools',
    license='MPL-2.0',
    packages=['fasta_tools'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
    )
