#!/usr/bin/env python3

"""
bookmark maker of pdf documents

by Novice Live, http:/novicelive.org/ :)

automatically add bookmarks to pdf documents according to the given regex.

you have to go through a somewhat painful debugging process if you want every added bookmark is exactly what you want and never omit where you desire it to be added.

PyPDF2 used to add bookmarks.
pdftotext from poppler used to extract text.

example regexes:
1. man pages
(?<=\bNAME\n)(.+|.+\n)+(?=\n(SYNOPSIS|DESCRIPTION))

the following ran into catastrophic backtracking when only the last part unmatch?
(?<=NAME\n)(.+|.+\n)+(?=\n(SYNOPSIS|DESCRIPTION))

example uses:
1. os x exploits and defense -- found 14 by the following regex: all 8 chapters + 6 others
Visit us at|Copyright(?=\s.\s2008)|^Technical Editor|Contributing Authors|^Contents|Chapter \d+\n\n(.+\n)+(?=Sol)|Chapter \d+\n\n.+\n|^Index

2.a guide to kernel exploitation -- found 20 by the following regex: all 4 parts + all 9 chapters + 7 others
(?<=PART\n)(\n.+)+|(?<=CHAPTER)\n\n.+((?=\nINF)|\n.+)|(?<=CHAPTER\n\n\d\n\n).+|^(Contents|Preface|Index)(?=\n[^\n])|^Foreword|^Acknowledgments|^About the Authors|^About the Technical Editor

3. zero day exploit -- found 18 by the following regex: all 10 chapters + 1 appendix + 7 others
^Chapter\s\d+\n(\n.+)+|Copyright|Acknowledgments|^Technical Editor|Foreword Contributor|Author Ackn.+|^Author|^Contents\n[^\n]|^Foreword(?=\n\n[A-Z]+)|^Appendix\n\n.+\n.+

4. open source fuzzing tools -- found 14 by the following regex: all 10 chapters + 4 others
^Chapter\s\d+\n((\n.+)+(?=\nSolutions in)|(\n.+)+)|Copyright(?=\s.\s2007)|Contributing Authors|^(Contents|Index)(?=\n[^\n])

5. hacking secret ciphers with python -- found 28 by the following regex: all 24 chapters + 4 others
(.+\n)+(?=Topics Covered)|Copyright|ABOUT THIS BOOK|TABLE OF CONTENTS|ABOUT THE AUTHOR

what is not good:
1. one page can have only one bookmark. so, re.search is used, instead of re.findall.

2. PyPDF2 fails upon secured pdf documents, even in which editing bookmarks is in fact allowed.

feb 7, 2015

1. for man pages, the aforementioned regexes will both fail on some pages. 
   so, i came up with this ugly regex: (?<=\nNAME\n)[\/_a-zA-RT-Z](.+|.+\n)+(?=\n(SYNOPSIS|DESC|CONFIG|\.))

2. minor changes. no use of str.lower() any more.

mar 1, 2015

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
    parser = argparse.ArgumentParser(description='automatically add bookmarks to pdf documents according to the given regex')
    parser.add_argument('pdf',
                        metavar='pdf_document',
                        help='the target pdf document to add bookmarks upon')
    parser.add_argument('-r', '--regex',
                        dest='regex',
                        metavar='reg_expr',
                        required=True,
                        help='use this regular expression to determine where to add a bookmark')
    parser.add_argument('-o', '--output',
                        metavar='pdf_output',
                        dest='output',
                        help='export the resulting pdf to the specified file name, instead of the default, output.pdf')
    parser.add_argument('-p', '--parse',
                        dest='parse',
                        action='store_const',
                        const=True,
                        default=False,
                        help='only parse and print result, do not add')
    parser.add_argument('-d', '--debug',
                        dest='debug',
                        action='store_const',
                        const=True,
                        default=False,
                        help='turn on debugging mode, which will display the raw matched strings of the specified regex. this should be used in conjunction with -p; well, this is not required.')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_const',
                        const=True,
                        default=False,
                        help='verbosely output displaying what is going on, and other error or warning information')

    args = parser.parse_args()

    if not args.output:
        args.output = 'output.pdf'

    # dev_null = open('/dev/null', 'w') # /dev/null :( sys.stdin :)

    # is redirecting to sys.stdin evil? this script does not use sys.stdin
    try:
        reader = PyPDF2.PdfFileReader(args.pdf, warndest=None if args.verbose else sys.stdin)
    except:
        print('could not read: {}'.format(args.pdf))
        if args.verbose:
            print(get_cur_error())
        exit()

    bookmarks = []
    
    for i in range(1, reader.numPages + 1):
        bookmark_title = parse_text(extract_text(args.pdf, i), args.regex, args.debug)
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

    sys.setrecursionlimit(2 * sys.getrecursionlimit()) # man3.pdf caused recursion maximum exceeded, let's take some risk
        
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
    this is only the parser for man pages. in other scenarios, you have to write your own parser

    + param str text: the text from a page to be determined whether we should add a bookmark to it or not
    + param str regex: the regex used to recognize a bookmark's title
    + param boolean debug: if true, print the original matched string, in order to improve debugging experience

    + return: if it should be bookmarked, return a list of the title and the page number. else return false
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
