"""
Copyright 2015-2017 Gu Zhengxiong <rectigu@gmail.com>
"""


from os.path import dirname, join

from setuptools import setup, find_packages


PROGRAM_NAME = 'pdfmark'
PACKAGE_NAME = PROGRAM_NAME.lower()


__author__ = 'Gu Zhengxiong'

_my_dir = dirname(__file__)

VERSION_FILE = 'VERSION.txt'


with open(join(_my_dir, PACKAGE_NAME, VERSION_FILE)) as stream:
    __version__ = stream.read().strip()

try:
    with open(join(_my_dir, 'requirements.txt')) as stream:
        _requirements = stream.read().splitlines()
except OSError:
    _requirements = []


setup(
    name=PROGRAM_NAME,
    author=__author__,
    author_email='rectigu@gmail.com',
    version=__version__,
    description='PDF Bookmark Adder',
    license='GPL',
    keywords='PDF Documents, Automatically Add Bookmarks, Regex',
    url='https://gitlab.com/imtheforce/{}'.format(PACKAGE_NAME),
    packages=find_packages(),
    package_data={
        PACKAGE_NAME: [VERSION_FILE],
    },
    install_requires=_requirements,
    entry_points={
        'console_scripts': [
            '{name}={name}.__main__:main'.format(name=PACKAGE_NAME),
        ]
    }
)
