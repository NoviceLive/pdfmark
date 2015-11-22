#!/usr/bin/env python3


"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import logging
import re

import PyPDF2

from .cli import parse_args
from .utils import extract_text


def main():
    """
    Start hacking.
    """
    args = parse_args()
    logging.basicConfig(
        format='%(levelname)-11s: %(message)s',
        level={
            0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG
        }[args.verbose % 3]
    )
    try:
        reader = PyPDF2.PdfFileReader(args.pdf)
    except Exception:
        logging.exception('could not read: %s', args.pdf)
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
        elif bookmark_title is None:
            return sys.EXIT_FAILURE
    if args.parse or args.verbose:
        if bookmarks:
            logging.info('found the following bookmarks')
        for i in bookmarks:
            logging.info(i)
    logging.info('parsing done. totally %s bookmarks',
                 len(bookmarks))

    if args.parse or args.verbose == 2:
        logging.warning('debugging or parsing mode, exiting...')
        return sys.EXIT_SUCCESS

    writer = PyPDF2.PdfFileWriter()
    try:
        for i in range(reader.numPages):
            writer.addPage(reader.getPage(i))
    except Exception:
        logging.exception('could not add page')
        return sys.EXIT_FAILURE
    try:
        for i in bookmarks:
            writer.addBookmark(i[1], i[0] - 1)
    except Exception:
        logging.exception('could not add bookmark')
        return sys.EXIT_FAILURE
    sys.setrecursionlimit(args.limit * sys.getrecursionlimit())
    try:
        with open(args.output, 'wb') as output:
            writer.write(output)
    except Exception:
        logging.exception('could not write: %s', args.output)
        return sys.EXIT_FAILURE

    logging.info('adding completed. happy reading. :)')


def parse_text(text, regex):
    """
    Parse the text against the given regular expression.
    """
    logging.debug('matching text\n%s', text)
    try:
        mat = re.search(regex, text)
    except Exception:
        logging.exception('regex error')
        return None
    if mat:
        logging.info('matched\n%s', mat.group(0))
        return mat.group(0)
    else:
        return False


if __name__ == '__main__':
    sys.exit(main())
