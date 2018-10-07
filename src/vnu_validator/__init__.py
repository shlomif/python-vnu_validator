__version__ = '0.1.0'

import os
from os.path import join
import re
import tempfile
from subprocess import call
import unittest


class VnuValidate:
    """docstring for VnuValidate"""
    def __init__(self, path, jar, non_xhtml_cb, skip_cb):
        self.path = path
        self.jar = jar
        self.non_xhtml_cb = non_xhtml_cb
        self.skip_cb = skip_cb

    def run(self):
        """docstring for run"""
        t = tempfile.TemporaryDirectory()
        for dirpath, _, fns in os.walk(self.path):
            dn = join(t.name, dirpath)
            os.makedirs(dn)
            for fn in fns:
                path = join(dirpath, fn)
                if self.skip_cb(path):
                    continue
                html = re.match(r'.*\.html?$', fn)
                if re.match('.*\\.xhtml$', fn) or (
                        html and not self.non_xhtml_cb(path)):
                    open(join(dn, re.sub('\.[^\.]*$', '.xhtml',
                                         fn)), 'w').write(
                        open(join(dirpath, fn)).read())
                elif html:
                    open(join(dn, fn), 'w').write(
                        open(path).read())

        return call(['java', '-jar', self.jar, '--Werror',
                     '--skip-non-html', t.name]) == 0


class VnuTest(unittest.TestCase):
    def vnu_test_dir(self, dir_, non_xhtml_cb, skip_cb):
        key = 'HTML_VALID_VNU_JAR'
        if key in os.environ:
            self.assertTrue(
                VnuValidate(dir_, os.environ[key], non_xhtml_cb,
                            skip_cb).run(),
                "passed validation")
        else:
            self.assertTrue(True, key + ' not set')
