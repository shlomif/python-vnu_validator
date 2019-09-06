__version__ = '0.1.0'

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from os.path import join
from subprocess import PIPE, Popen

from six.moves.urllib.parse import urlparse


DONT_DELETE_TEMP = True if int(os.getenv('VNU_DONT_DELETE_TEMP', '0')) == 1 else False


def _temp_rmtree(tname):
    if DONT_DELETE_TEMP:
        sys.stderr.write('Keeping %s\n' % (tname))
    else:
        shutil.rmtree(tname)


class VnuValidate(object):
    """
    Run the Nu HTML Validator on a directory tree of XHTML5 and HTML5 files.

    :param path the path of the root directory
    :param jar path to the Java .jar of the Nu validator
    :param non_xhtml_cb A callback that accepts a path and returns whether it
    is not XHTML
    :param skip_cb Return whether a path should be skipped entirely
    :param cache_path An optional path to a cache file to speed up
    subsequent runs

    Set the VNU_DONT_DELETE_TEMP to 1 to avoid deleting the temp dir
    (for debugging).
    """
    def __init__(self, path, jar, non_xhtml_cb, skip_cb, cache_path=None):
        self.path = path
        self.jar = jar
        self.non_xhtml_cb = non_xhtml_cb
        self.skip_cb = skip_cb
        self.cache_path = cache_path

    def _digest(self, content):
        """docstring for _digest"""
        m = hashlib.sha256()
        m.update(content)
        return m.hexdigest()

    def _empty_cache(self):
        return {'html': {}, 'xhtml': {}}

    _TRIM_RE = re.compile('^(?:\\./)?')
    _HTML_SUF_RE = re.compile(r'.*\.html?$')
    _XHTML_SUF_RE = re.compile(r'.*\.xhtml?$')
    _SUF_RE = re.compile(r'\.[^\.]*$')

    def run(self):
        """
        :returns boolean for success or failure.
        """
        # t = tempfile.TemporaryDirectory()
        tname = tempfile.mkdtemp()
        # t = VnuValidate(0, 0, 0, 0)
        # t.name = "/tmp/zjzj"
        whitelist = self._empty_cache()
        try:
            if self.cache_path:
                whitelist = json.load(
                    open(self.cache_path, 'rb'))['vnu_valid']['cache'][
                            'sha256']
        except FileNotFoundError:
            pass
        which = {}
        greylist = self._empty_cache()

        def _mytrim(s):
            return self._TRIM_RE.sub('', s)

        for dirpath, _, fns in os.walk(self.path):
            dn = _mytrim(join(tname, _mytrim(dirpath)))
            os.makedirs(dn)
            for fn in fns:
                path = _mytrim(join(dirpath, fn))
                if self.skip_cb(path):
                    continue
                html = self._HTML_SUF_RE.match(fn)
                out_fn = None
                if self._XHTML_SUF_RE.match(fn) or (
                        html and not self.non_xhtml_cb(path)):
                    out_fn = self._SUF_RE.sub('.xhtml', fn)
                elif html:
                    out_fn = fn

                if out_fn:
                    c = open(path, 'rb').read()
                    d = self._digest(c)
                    format_ = 'html' if html else 'xhtml'
                    if d not in whitelist[format_]:
                        fn = join(dn, out_fn)
                        open(fn, 'wb').write(c)
                        which[fn] = format_
                        greylist[format_][d] = True

        cmd = ['java', '-jar', self.jar, '--format', 'json', '--Werror',
               '--skip-non-html', tname]
        print(" ".join(cmd))
        # import sys
        # sys.exit(0)
        verdict = False
        ret = Popen(cmd, stderr=PIPE)
        ret.wait()
        text = ret.stderr.read()
        data = json.loads(text)
        blacklist = self._empty_cache()
        found = set()
        for msg in data['messages']:
            print(msg)
            url = msg['url']
            fn = urlparse(url).path
            if fn not in found:
                found.add(fn)
                d = self._digest(open(fn, 'rb').read())
                blacklist[which[fn]][d] = True
        for format_ in ['html', 'xhtml']:
            for k in list(greylist[format_].keys()):
                if k not in blacklist[format_]:
                    whitelist[format_][k] = True
        if self.cache_path:
            json.dump({'vnu_valid': {'cache': {'sha256': whitelist}}},
                      open(self.cache_path, 'w'))
        verdict = (len(blacklist['html']) + len(blacklist['xhtml']) == 0)
        _temp_rmtree(tname)
        return verdict


class VnuSingleFileValidate(object):
    """
    Run the Nu HTML Validator on a single file

    :param path the path of the single file
    :param jar path to the Java .jar of the Nu validator
    :param non_xhtml Whether it is not xhtml.
    subsequent runs
    """
    def __init__(self, path, jar, non_xhtml):
        self.path = path
        self.jar = jar
        self.non_xhtml_cb = lambda path: non_xhtml

    def run(self):
        """
        :returns boolean for success or failure.
        """
        # t = tempfile.TemporaryDirectory()
        tname = tempfile.mkdtemp()
        open(join(tname, "foo.html"), 'wb').write(open(self.path, 'rb').read())
        verdict = VnuValidate(tname, self.jar, self.non_xhtml_cb, lambda p: False).run()
        _temp_rmtree(tname)
        return verdict


class VnuTest(unittest.TestCase):
    """
    One can find some examples for this here:

    """
    def vnu_test_dir(self, path, non_xhtml_cb, skip_cb, cache_path=None):
        """
        A unit test helper for checking a directory tree.
        :param path the path of the root directory
        :param non_xhtml_cb A callback that accepts a path and returns whether
        it
        :param skip_cb Return whether a path should be skipped entirely
        :param cache_path An optional path to a cache file to speed up
        subsequent runs

        Uses an environment variable HTML_VALID_VNU_JAR that points to the
        validator .jar (see https://github.com/validator/validator/ ).
        """
        key = 'HTML_VALID_VNU_JAR'
        if key in os.environ:
            self.assertTrue(
                VnuValidate(path, os.environ[key], non_xhtml_cb,
                            skip_cb, cache_path).run(),
                "passed validation")
        else:
            self.assertTrue(True, key + ' not set')
