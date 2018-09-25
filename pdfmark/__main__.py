#!/usr/bin/env python3


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


from logging import getLogger
import sys
import re
import subprocess

from pycliprog.argparse import Prog, ExitFailure
from PyPDF2 import PdfFileReader, PdfFileWriter


logger = getLogger(__name__)


def main():
    PdfMarkProg().start()


class PdfMarkProg(Prog):
    def main(self):
        logger.debug('using regex: %s', self.args.regex)
        try:
            reader = PdfFileReader(self.args.pdf)
        except Exception:
            raise ExitFailure('could not read: %s', self.args.pdf)

        bookmarks = []
        for i in range(1, reader.numPages+1):
            bookmark_title = parse_text(extract_text(self.args.pdf, i), self.args.regex)
            if bookmark_title:
                bookmark_title = bookmark_title.replace('\n', ' ').strip()
                logger.info('found title at: %s %s', i, bookmark_title)
                bookmarks.append([i, bookmark_title])
            elif bookmark_title is None:
                raise ExitFailure('bookmark_title is None')
        logger.info('parsing done. totally %s bookmarks', len(bookmarks))

        if self.args.parse:
            logger.warning('debugging or parsing mode, exiting...')
            return

        writer = PdfFileWriter()
        try:
            for i in range(reader.numPages):
                writer.addPage(reader.getPage(i))
        except Exception:
            raise ExitFailure('could not add page')

        try:
            for i in bookmarks:
                writer.addBookmark(i[1], i[0] - 1)
        except Exception:
            raise ExitFailure('could not add bookmark')

        sys.setrecursionlimit(self.args.limit * sys.getrecursionlimit())
        try:
            with open(self.args.output, 'wb') as output:
                writer.write(output)
        except Exception:
            raise ExitFailure('could not write: %s', self.args.output)

        logger.info('adding completed. happy reading. :)')

    def add_args(self):
        self.parser.add_argument(
            'pdf', metavar='PDF',
            help='the original PDF to add bookmarks upon')
        self.parser.add_argument(
            '-r', '--regex', required=True,
            help='use this regular expression to find bookmarks')
        self.parser.add_argument(
            '-o', '--output', default='output.pdf',
            help='output PDF using this file name')
        self.parser.add_argument(
            '-l', '--limit', type=int, default=3,
            help='multiply recursion limit by this number')
        self.parser.add_argument(
            '-p', '--parse', action='store_true',
            help='only parse and print result, do not add')

    @property
    def name(self):
        return 'PDF Bookmark Adder'

    @property
    def version(self):
        return '{}, version {}\n{}'.format(self.name, self.read_version(__file__), """
Copyright 2015-2018 Gu Zhengxiong <rectigu@gmail.com>""".strip())


def extract_text(pdf_file, page_number):
    """
    Extract the text from the PDF file.
    """
    # pdftotext
    # -layout              : maintain original physical layout
    # -raw                 : keep strings in content stream order
    args = [
        'pdftotext', pdf_file,
        '-raw',
        '-f', str(page_number),
        '-l', str(page_number),
        '-'
    ]
    logger.debug('pdftotext args: %s', args)
    return subprocess.check_output(args).decode('utf-8')


def parse_text(text, regex):
    """
    Parse the text against the given regular expression.
    """
    logger.debug('matching text\n%s', text)
    try:
        mat = re.search(regex, text)
    except Exception:
        logger.exception('regex error')
        return None
    if mat:
        logger.debug('matched\n%s', mat.group(0))
        return mat.group(0)
    else:
        return False


if __name__ == '__main__':
    main()
