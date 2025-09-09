#!/usr/bin/env python
"""
dollarReplace.py

Created by Steve McMahon on 2009-08-13.
Copyright (c) 2009 Plone Foundation.
"""

from AccessControl import Unauthorized
from plone.stringinterp.interfaces import IStringInterpolator
from plone.stringinterp.interfaces import IStringSubstitution
from Products.CMFCore.interfaces import IContentish
from zope.component import adapter
from zope.component import ComponentLookupError
from zope.component import getAdapter
from zope.interface import implementer

import string


_marker = "_bad_"


class LazyDict:
    """cached lookup via adapter"""

    def __init__(self, context):
        self.context = context
        self._cache = {}

    def __getitem__(self, key):
        if key and key[0] not in ["_", "."]:
            res = self._cache.get(key)
            if res is None:
                try:
                    res = getAdapter(self.context, IStringSubstitution, key)()
                except ComponentLookupError:
                    res = _marker
                except Unauthorized:
                    res = "Unauthorized"

                self._cache[key] = res

            if res != _marker:
                return res

        raise KeyError(key)


@implementer(IStringInterpolator)
@adapter(IContentish)
class Interpolator:
    def __init__(self, context):
        self._ldict = LazyDict(context)

    def __call__(self, s):
        return string.Template(s).safe_substitute(self._ldict)
