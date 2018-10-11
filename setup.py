"""
Copyright 2015-2018 Gu Zhengxiong <rectigu@gmail.com>

This file is part of pdfmark.

pdfmark is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pdfmark is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pdfmark.  If not, see <http://www.gnu.org/licenses/>.
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

with open(join(_my_dir, 'README.rst')) as stream:
    long_description = stream.read()


setup(
    name=PROGRAM_NAME,
    author=__author__,
    author_email='rectigu@gmail.com',
    version=__version__,
    description='PDF Bookmark Adder',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='GPL-3',
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
