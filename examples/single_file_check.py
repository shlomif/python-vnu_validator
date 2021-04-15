#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Shlomi Fish < https://www.shlomifish.org/ >
#
# Licensed under the terms of the MIT license.
from vnu_validator import VnuSingleFileValidate
import os
import sys

fn = sys.argv.pop(1)
print('fn =', fn)
JAR = os.environ['HTML_VALID_VNU_JAR']
non_xhtml = (not (fn.endswith(".xhtml")))
obj = VnuSingleFileValidate(path=fn, jar=JAR, non_xhtml=non_xhtml)
obj.run()
