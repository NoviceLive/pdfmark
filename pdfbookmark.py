#!/usr/bin/env python3


"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


__version__ = 'pdfbookmark 0.1.0'


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import argparse
import logging
import subprocess
import re

import PyPDF2


def main(args):
    try:
        reader = PyPDF2.PdfFileReader(args.pdf)
    except:
        logging.exception('could not read: {}'.format(args.pdf))
        return sys.EXIT_FAILURE

    bookmarks = []
    for i in range(1, reader.numPages + 1):
        bookmark_title = parse_text(
            extract_text(args.pdf, i),
            args.regex
        )
        if bookmark_title:
            bookmarks.append(
                [i, bookmark_title.replace('\n', ' ').strip()]
            )
        elif bookmark_title == None:
            exit()

    if args.parse or args.verbose:
        if bookmarks:
            logging.info('found the following bookmarks')
        for i in bookmarks:
            logging.info(i)

    logging.info(
        'parsing done. totally {} bookmarks'.format(
        len(bookmarks)
        )
    )

    if args.parse or args.verbose == 2:
        logging.warning('debugging or parsing mode, exiting...')
        return sys.EXIT_SUCCESS

    writer = PyPDF2.PdfFileWriter()
    try:
        for i in range(reader.numPages):
            writer.addPage(reader.getPage(i))
    except:
        logging.exception('could not add page')
        return sys.EXIT_FAILURE

    try:
        for i in bookmarks:
            writer.addBookmark(i[1], i[0] - 1)
    except:
        logging.exception('could not add bookmark')
        return sys.EXIT_FAILURE

    sys.setrecursionlimit(args.limit * sys.getrecursionlimit())

    try:
        with open(args.output, 'wb') as output:
            writer.write(output)
    except:
        logging.exception('could not write: {}'.format(args.output))
        return sys.EXIT_FAILURE

    logging.info('adding completed. happy reading. :)')


def parse_text(text, regex):
    logging.debug('matching text\n{}'.format(text))
    try:
        mat =  re.search(regex, text)
    except:
        logging.exception('regex error')
        return None
    if mat:
        logging.info('matched\n{}'.format(mat.group(0)))
        return mat.group(0)
    else:
        return False


def extract_text(pdf_file, page_number):
    return subprocess.check_output(
        [
            'pdftotext',
            pdf_file,
            '-f',
            str(page_number),
            '-l',
            str(page_number),
            '-'
        ]
    ).decode('utf-8')


def parse_args():
    parser = argparse.ArgumentParser(
        description='PDF Bookmark Maker')
    parser.add_argument(
        'pdf', metavar='PDF',
        help='the original PDF to add bookmarks upon')
    parser.add_argument(
        '-r', '--regex', required=True,
        help='use this regular expression to find bookmarks')
    parser.add_argument(
        '-o', '--output', default='output.pdf',
        help='output PDF using this file name')
    parser.add_argument(
        '-l', '--limit', type=int, default=3,
        help='multiply recursion limit by this number')
    parser.add_argument(
        '-p', '--parse', action='store_true',
        help='only parse and print result, do not add')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='turn on verbose mode, -vv for debugging mode')
    parser.add_argument(
        '-V', '--version', action='version',version=__version__)

    return parser.parse_args()


def start_main():
    args = parse_args()

    logging.basicConfig(
        format='%(levelname)-11s: %(message)s',
        level={
            0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG
        }[args.verbose % 3]
    )

    sys.exit(main(args))


if __name__ == '__main__':
    start_main()
