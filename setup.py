from setuptools import setup


setup(
    name='pdfmark',
    version='0.1.0',
    py_modules=['pdfbookmark'],
    install_requires = ['PyPDF2'],

    entry_points={
        'console_scripts' : ['pdfbookmark=pdfbookmark:start_main']
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    author='Gu Zhengxiong',
    author_email='rectigu@gmail.com',
    description='PDF Bookmark Adder',
    keywords='PDF Documents, Automatically Add Bookmarks, Regex',
    license='GPL',
    url='https://github.com/NoviceLive/pdfbookmark'
)
