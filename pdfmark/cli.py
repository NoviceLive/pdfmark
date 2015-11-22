"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import argparse


__version__ = 'pdfbookmark 0.1.0'


def parse_args():
    """
    Parse th arguments.
    """
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
        '-V', '--version', action='version', version=__version__)
    return parser.parse_args()
