#!/usr/bin/env bash


#
# Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>
#


TARGETS='setup.py run.py ./pdfmark'
pylint $TARGETS
cloc $TARGETS
