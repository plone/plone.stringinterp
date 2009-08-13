#!/usr/bin/env python
# encoding: utf-8
"""
adapters.py

Created by Steve McMahon on 2009-08-12.
Copyright (c) 2009 Plone Foundation.
"""

from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.interfaces import \
    IContentish, IMinimalDublinCore

from interfaces import IStringSubstitution


class BaseSubstitution(object):
    implements(IStringSubstitution)

    def __init__(self, context):
        self.context = context


class UrlSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    def __call__(self):
        return self.context.absolute_url()


class TitleSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return self.context.Title()


class DescriptionSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return self.context.Description()


class TypeSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return self.context.Type()
