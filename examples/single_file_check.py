#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Shlomi Fish < https://www.shlomifish.org/ >
#
# Licensed under the terms of the MIT license.
"""
python3 ~/progs/python/vnu/python-vnu_validator/examples/single_file_check.py \
    --filename dest/post-incs/t2/open-source/resources/databases-list/index.xhtml
"""

import argparse
from vnu_validator import VnuSingleFileValidate
import os
import sys


class CliApp:
    """docstring for GenMulti"""
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog='PROG',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--filename', type=str, required=True,
                            help='input filename')
        # parser.add_argument('idxs', nargs='+', default=[],
        #                     help='indexes')
        args = parser.parse_args(argv[1:])
        self.fn = args.filename

    def run(self):
        """docstring for run"""
        fn = self.fn
        print('fn =', fn)
        JAR = os.environ['HTML_VALID_VNU_JAR']
        non_xhtml = (not (fn.endswith(".xhtml")))
        obj = VnuSingleFileValidate(path=fn, jar=JAR, non_xhtml=non_xhtml)
        return obj.run()


if __name__ == "__main__":
    sys.exit(CliApp(sys.argv).run())
