pdfmark - One Of My Most Initial Python Projects
================================================


.. image:: https://img.shields.io/pypi/v/pdfmark.svg
   :target: https://pypi.python.org/pypi/pdfmark


PDF Bookmark Adder


Official Mirrors
----------------

- https://gitlab.com/imtheforce/pdfmark
- https://bitbucket.org/fourthorigin/pdfmark
- https://github.com/NoviceLive/pdfmark


Features
--------

Automatically add bookmarks to pdf documents
according to the given regex.

You have to go through a somewhat painful debugging process
if you want every added bookmark is exactly what you want
and never omit where you desire it to be added.


Installation
------------

``pip install pdfmark``


Dependencies
------------

- ``PyPDF2``, which can be installed via pip
- ``pdftotext``, which is available from the packages listed below

  - Fedora, ``poppler-utils``
  - Arch, ``poppler``


Usage
-----

See ``samples.txt``.

Also see this real world case,
man2pdf, https://github.com/NoviceLive/man2pdf,
for which this quick and dirty script was written.

And ``./pdfmark --help``.


TODO
----

Support heirarchical bookmarks.


License
-------

See ``LICENSE.txt``.
