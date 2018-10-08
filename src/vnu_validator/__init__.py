__version__ = '0.1.0'

import os
from os.path import join
import re
import tempfile
from subprocess import call
import unittest


class VnuValidate:
    """
    Run the Nu HTML Validator on a directory tree of XHTML5 and HTML5 files.

    :param path the path of the root directory
    :param jar path to the Java .jar of the Nu validator
    :param non_xhtml_cb A callback that accepts a path and returns whether it
    is not XHTML
    :param skip_cb Return whether a path should be skipped entirely
    """
    def __init__(self, path, jar, non_xhtml_cb, skip_cb):
        self.path = path
        self.jar = jar
        self.non_xhtml_cb = non_xhtml_cb
        self.skip_cb = skip_cb

    def run(self):
        """
        :returns boolean for sucess or failure.
        """
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
    """
    One can find some examples for this here:

    * https://github.com/shlomif/better-scm/blob/master/Tests/validate-html-using-vnu.py
    * https://github.com/shlomif/perl-begin/blob/master/Tests/validate-html-using-vnu.py
    * https://github.com/shlomif/shlomi-fish-homepage/blob/master/Tests/validate-html-using-vnu.py
    """
    def vnu_test_dir(self, path, non_xhtml_cb, skip_cb):
        """
        A unit test helper for checking a directory tree.
        :param path the path of the root directory
        :param non_xhtml_cb A callback that accepts a path and returns whether
        it
        :param skip_cb Return whether a path should be skipped entirely

        Uses an environment variable HTML_VALID_VNU_JAR that points to the
        validator .jar (see https://github.com/validator/validator/ ).
        """
        key = 'HTML_VALID_VNU_JAR'
        if key in os.environ:
            self.assertTrue(
                VnuValidate(path, os.environ[key], non_xhtml_cb,
                            skip_cb).run(),
                "passed validation")
        else:
            self.assertTrue(True, key + ' not set')
