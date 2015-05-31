pdfbookmark

bookmark maker of pdf documents
automatically add bookmarks to pdf documents according to the given regex.

you have to go through a somewhat painful debugging process
if you want every added bookmark is exactly what you want
and never omit where you desire it to be added.

PyPDF2 used to add bookmarks.
pdftotext from poppler used to extract text.

example regexes:
1. man pages
(?<=\nNAME\n)[\/_a-zA-RT-Z](.+|.+\n)+(?=\n(SYNOPSIS|DESC|CONFIG|\.))

the following ran into catastrophic backtracking
when only the last part unmatch?
(?<=NAME\n)(.+|.+\n)+(?=\n(SYNOPSIS|DESCRIPTION))

example uses:
1. os x exploits and defense
found 14 by the following regex: all 8 chapters + 6 others

Visit us at|Copyright(?=\s.\s2008)|^Technical Editor|Contributing Authors|^Contents|Chapter \d+\n\n(.+\n)+(?=Sol)|Chapter \d+\n\n.+\n|^Index

2.a guide to kernel exploitation
found 20 by the following regex: all 4 parts + all 9 chapters + 7 others

(?<=PART\n)(\n.+)+|(?<=CHAPTER)\n\n.+((?=\nINF)|\n.+)|(?<=CHAPTER\n\n\d\n\n).+|^(Contents|Preface|Index)(?=\n[^\n])|^Foreword|^Acknowledgments|^About the Authors|^About the Technical Editor

3. zero day exploit
found 18 by the following regex: all 10 chapters + 1 appendix + 7 others

^Chapter\s\d+\n(\n.+)+|Copyright|Acknowledgments|^Technical Editor|Foreword Contributor|Author Ackn.+|^Author|^Contents\n[^\n]|^Foreword(?=\n\n[A-Z]+)|^Appendix\n\n.+\n.+

4. open source fuzzing tools
found 14 by the following regex: all 10 chapters + 4 others

^Chapter\s\d+\n((\n.+)+(?=\nSolutions in)|(\n.+)+)|Copyright(?=\s.\s2007)|Contributing Authors|^(Contents|Index)(?=\n[^\n])

5. hacking secret ciphers with python
found 28 by the following regex: all 24 chapters + 4 others

(.+\n)+(?=Topics Covered)|Copyright|ABOUT THIS BOOK|TABLE OF CONTENTS|ABOUT THE AUTHOR

what is not good:
1. one page can have only one bookmark.
   so, re.search is used, instead of re.findall.

2. PyPDF2 fails upon secured pdf documents,
   even in which editing bookmarks is in fact allowed.
