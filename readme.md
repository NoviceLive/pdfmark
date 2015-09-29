# pdfbookmark

PDF Bookmark Adder

## Features

Automatically add bookmarks to pdf documents
according to the given regex.

You have to go through a somewhat painful debugging process
if you want every added bookmark is exactly what you want
and never omit where you desire it to be added.

## Installation

```
sudo pip install pdfmark
```

## Dependencies

- PyPDF2, which can be installed via pip
- pdftotext, which is available from the package `poppler-utils`

## Usage

See samples.txt

Also see this real world case,
[man2pdf](https://github.com/NoviceLive/man2pdf),
for which this quick and dirty script was written.

And `./pdfbookmark --help`.

## TODO

Support heirarchical bookmarks.

## License

GPL
