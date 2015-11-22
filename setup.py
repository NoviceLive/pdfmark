"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


from setuptools import setup


setup(
    name='pdfmark',
    version='0.1.0',
    packages=['pdfmark'],
    entry_points={
        'console_scripts' : ['pdfmark=pdfmark.start:main']
    },

    author='Gu Zhengxiong',
    author_email='rectigu@gmail.com',
    description='PDF Bookmark Adder',
    keywords='PDF Documents, Automatically Add Bookmarks, Regex',
    license='GPL',
    url='https://github.com/NoviceLive/pdfbookmark',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
