#!/usr/bin/env python3


"""
Bookmark Maker Of PDF Documents

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


import sys
import subprocess
import argparse
import re
import traceback

import PyPDF2


def main():
    args = parse_args()

    if not args.output:
        args.output = 'output.pdf'

    # is redirecting to sys.stdin evil? this script does not use sys.stdin
    try:
        reader = PyPDF2.PdfFileReader(
            args.pdf,
            warndest=None if args.verbose else sys.stdin
        )
    except:
        print('could not read: {}'.format(args.pdf))
        if args.verbose:
            traceback.print_exc()
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
        print('add page error')
        traceback.print_exc()
        exit()

    try:
        [writer.addBookmark(i[1], i[0] - 1) for i in bookmarks]
    except:
        print('add bookmark error')
        traceback.print_exc()
        exit()

    # some pdf files caused recursion maximum exceeded, let's take some risk
    sys.setrecursionlimit(2 * sys.getrecursionlimit())

    try:
        with open(args.output, 'wb') as output:
            writer.write(output)
    except:
        print('could not write: {}'.format(args.output))
        if args.verbose:
            traceback.print_exc()
        exit()

    print('adding completed. happy reading. :)')

    # dev_null.close()


def parse_text(text, regex, debug):
    if debug:
            print('matching text\n{}'.format(text))

    try:
        mat =  re.search(regex, text)
    except:
        print('regex error')
        traceback.print_exc()
        return None

    if mat:
        print('matched\n{}'.format(mat.group(0)))
        return mat.group(0)

    else:
        return False


def extract_text(pdf_file, page_number):
    return subprocess.check_output(
        ['pdftotext',
         pdf_file,
         '-f', str(page_number),
         '-l', str(page_number),
         '-']
    ).decode('utf-8')


def parse_args():
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

    return parser.parse_args()


if __name__ == '__main__':
    main()
