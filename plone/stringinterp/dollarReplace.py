#!/usr/bin/env python
# encoding: utf-8
"""
dollarReplace.py

Created by Steve McMahon on 2009-08-13.
Copyright (c) 2009 Plone Foundation.
"""

import re

from zope.interface import implements
from zope.component import adapts, getAdapter, ComponentLookupError

from Products.CMFCore.interfaces import IContentish

from plone.memoize.instance import memoize

from interfaces import IStringSubstitution, IStringInterpolator


# # regular expression for dollar-sign variable replacement.
# we want to find ${identifier} patterns
dollarRE = re.compile(r"\$\{(\S+?)\}")


class Interpolator(object):
    adapts(IContentish)
    implements(IStringInterpolator)

    def __init__(self, context):
        self.context = context
        self._cache = {}

    def __call__(self, s):
        return dollarRE.sub(self.repl, s)

    def repl(self, mo):
        key = mo.group(1)
        if key and key[0] not in ['_','.']:
            res = self._cache.get(key)
            if res is None:
                try:
                    res = getAdapter(self.context, IStringSubstitution, key)()
                except ComponentLookupError:
                    res = u'???'
                self._cache[key] = res
            return res
        return u''
