#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the MIT license.

import sys

from pydistman import DistManager


class Derived(DistManager):
    """docstring for Derived"""
    def _build_only_command_custom_steps(self):
        for fn in self._src_glob("tests/data/*"):
            self._dest_append(fn)
        return


try:
    cmd = sys.argv.pop(1)
except IndexError:
    cmd = 'build'

dist_name = "vnu_validator"

obj = Derived(
    dist_name=dist_name,
    dist_version="0.10.0",
    project_name=dist_name,
    project_short_description="Python Wrapper for the v.Nu HTML Validator",
    release_date="2021-12-20",
    project_year="2020",
    aur_email="shlomif@cpan.org",
    project_email="shlomif@cpan.org",
    full_name="Shlomi Fish",
    github_username="shlomif",
    filter_test_reqs=True,
)
obj.run_command(cmd=cmd, args=[])
