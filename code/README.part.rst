========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-vnu_validator/badge/?style=flat
    :target: https://readthedocs.org/projects/python-vnu_validator
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/shlomif/python-vnu_validator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/shlomif/python-vnu_validator

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/shlomif/python-vnu_validator?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/shlomif/python-vnu_validator

.. |requires| image:: https://requires.io/github/shlomif/python-vnu_validator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/shlomif/python-vnu_validator/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/shlomif/python-vnu_validator/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/shlomif/python-vnu_validator

.. |version| image:: https://img.shields.io/pypi/v/vnu-validator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/vnu-validator

.. |commits-since| image:: https://img.shields.io/github/commits-since/shlomif/python-vnu_validator/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/shlomif/python-vnu_validator/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/vnu-validator.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/vnu-validator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/vnu-validator.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/vnu-validator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/vnu-validator.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/vnu-validator


.. end-badges

Python Wrapper for the v.Nu HTML Validator. It allows one to recursively test
a directory
of XHTML5 or HTML5 files for HTML validity (see
https://www.shlomifish.org/philosophy/computers/web/validate-your-html/ and
https://github.com/validator/validator/ ). It provides a caching feature for
speedup of subsequent runs.

See:

::
   pydoc vnu-validator

* Free software: MIT license

Installation
============

::

    pip install vnu-validator

Documentation
=============


https://python-vnu_validator.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
