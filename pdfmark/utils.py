"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
"""


import subprocess


def extract_text(pdf_file, page_number):
    """
    Extract the text from the PDF file.
    """
    return subprocess.check_output(
        [
            'pdftotext', pdf_file,
            '-f', str(page_number),
            '-l', str(page_number),
            '-'
        ]
    ).decode('utf-8')
