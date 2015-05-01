#!/usr/bin/env python3


"""
bookmark maker of pdf documents

by Novice Live, http:/novicelive.org/ :)

Copyright (C) 2015  Gu Zhengxiong

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import sys
import subprocess
import argparse
import re

import PyPDF2


def main():
    parser = argparse.ArgumentParser(
        description="""automatically add bookmarks to pdf documents
according to the given regex""")

    parser.add_argument('pdf', metavar='pdf_document',
                        help='the target pdf document to add bookmarks upon')

    parser.add_argument('-r', '--regex', dest='regex', metavar='reg_expr',
                        required=True,
                        help="""use this regular expression to determine
 where to add a bookmark""")

    parser.add_argument('-o', '--output', metavar='pdf_output', dest='output',
                        help="""export the resulting pdf to the specified
file name, instead of the default, output.pdf""")

    parser.add_argument('-p', '--parse', dest='parse',
                        action='store_true',
                        help='only parse and print result, do not add')

    parser.add_argument('-d', '--debug',
                        dest='debug',
                        action='store_true',
                        help="""turn on debugging mode,
which will display the raw matched strings of the specified regex.
this should be used in conjunction with -p; well, this is not required.""")

    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help="""verbosely output displaying what is going on,
and other error or warning information""")

    args = parser.parse_args()

    if not args.output:
        args.output = 'output.pdf'

    # dev_null = open('/dev/null', 'w') # /dev/null :( sys.stdin :)

    # is redirecting to sys.stdin evil? this script does not use sys.stdin
    try:
        reader = PyPDF2.PdfFileReader(
            args.pdf,
            warndest=None if args.verbose else sys.stdin
        )
    except:
        print('could not read: {}'.format(args.pdf))
        if args.verbose:
            print(get_cur_error())
        exit()

    bookmarks = []

    for i in range(1, reader.numPages + 1):
        bookmark_title = parse_text(
            extract_text(args.pdf, i), args.regex, args.debug
        )
        if bookmark_title:
            bookmarks.append([i, bookmark_title.replace('\n', ' ').strip()])
        elif bookmark_title == None:
            exit()

    if args.parse or args.verbose:
        if bookmarks:
            print('found the following bookmarks')
        [print(i) for i in bookmarks]

    print('parsing done. totally {} bookmarks'.format(len(bookmarks)))

    if args.parse or args.debug:
        exit()

    writer = PyPDF2.PdfFileWriter()
    try:
        [writer.addPage(reader.getPage(i)) for i in range(reader.numPages)]
    except:
        print('add page error: {}'.format(get_cur_error()))
        exit()

    try:
        [writer.addBookmark(i[1], i[0] - 1) for i in bookmarks]
    except:
        print('add bookmark error: {}'.format(get_cur_error()))
        exit()

    # some pdf files caused recursion maximum exceeded, let's take some risk
    sys.setrecursionlimit(2 * sys.getrecursionlimit())

    try:
        with open(args.output, 'wb') as output:
            writer.write(output)
    except:
        print('could not write: {}'.format(args.output))
        if args.verbose:
            print(get_cur_error())
        exit()

    print('adding completed. happy reading. :)')

    # dev_null.close()


def parse_text(text, regex, debug):
    """
    parse text in order to recognize whether to add a bookmark here
    this is only the parser for man pages.
    in other scenarios, you have to write your own parser

    + param str text: the text from a page to be determined
    whether we should add a bookmark to it or not

    + param str regex: the regex used to recognize a bookmark's title

    + param boolean debug: if true, print the original matched string,
    in order to improve debugging experience

    + return: if it should be bookmarked, return a list of the title
    and the page number. else return false

    + rtype: list or boolean
    """
    if debug:
            print('matching text\n{}'.format(text))

    try:
        mat =  re.search(regex, text)
    except:
        print('regex error: {}'.format(get_cur_error()))
        return None

    if mat:
        print('matched\n{}'.format(mat.group(0)))
        return mat.group(0)

    else:
        return False


def extract_text(pdf_file, page_number):
    """
    extract text in the specified page of the specified document via pdftotext

    + param str pdf_file: the document's name or path
    + param int page_number: which page to extract

    + return: the text extracted from that page
    + rtype: str
    """
    return subprocess.check_output(
        ['pdftotext',
         pdf_file,
         '-f', str(page_number),
         '-l', str(page_number),
         '-']
    ).decode('utf-8')


def get_cur_error():
    """
    get current error information and return the prompt string

    + return: the error prompt string. None if no error
    + rtype: str or boolean
    """
    return sys.exc_info()[1]


if __name__ == '__main__':
    main()
