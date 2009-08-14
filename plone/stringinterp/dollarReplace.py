#!/usr/bin/env python
# encoding: utf-8
"""
dollarReplace.py

Created by Steve McMahon on 2009-08-13.
Copyright (c) 2009 Plone Foundation.
"""

import re

from zope.component import getAdapter, queryAdapter, ComponentLookupError

from interfaces import IStringSubstitution


# # regular expression for dollar-sign variable replacement.
# we want to find ${identifier} patterns
dollarRE = re.compile(r"\$\{(\S+?)\}")


class Interpolator(object):

    def __init__(self, context):
        self.context = context

    def __call__(self, s):
        return dollarRE.sub(self.repl, s)

    def repl(self, mo):
        key = mo.group(1)
        if key and key[0] not in ['_','.']:
            try:
                return getAdapter(self.context, IStringSubstitution, key)()
            except ComponentLookupError:
                pass
        return '???'
