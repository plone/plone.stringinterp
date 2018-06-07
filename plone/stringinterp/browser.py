#!/usr/bin/env python
# encoding: utf-8
"""
interfaces.py

Created by Steve McMahon on 2009-09-20.
Copyright (c) 2009 Plone Foundation.
"""

from zope.component import getSiteManager

from Products.Five import BrowserView

from plone.stringinterp.interfaces import IStringSubstitution
from plone.stringinterp import _


def find_adapters(reg):
    for a in reg.registeredAdapters():
        if len(a.required) == 1 and IStringSubstitution.implementedBy(a.factory):
            yield a
    for base in reg.__bases__:
        for a in find_adapters(base):
            yield a


class SubstitutionInfo(BrowserView):
    """
    Browser view support for listing IStringSubstitution
    adapters.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def substitutionList(self):
        """
        returns sequence:
        [ {'category':categoryTitle,
           'items':[{'id':subId, 'description':subDescription}, ...]), ...  ]
        """

        # rearrange into categories
        categories = {}
        for a in find_adapters(getSiteManager()):
            id = a.name
            cat = getattr(a.factory, 'category', _(u'Miscellaneous'))
            desc = getattr(a.factory, 'description', u'')
            categories.setdefault(cat, []).append(
              {'id': id, 'description': desc})

        # rearrange again into a sorted list
        res = []
        keys = categories.keys()
        # sort, ignoring case
        for key in sorted(keys, key=lambda s: s.lower()):
            acat = categories[key]
            # sort by id, ignoring case
            acat = sorted(acat, key=lambda i: i['id'].lower())
            res.append({'category': key, 'items': acat})

        return res
