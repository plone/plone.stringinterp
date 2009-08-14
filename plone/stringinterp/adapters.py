#!/usr/bin/env python
# encoding: utf-8
"""
adapters.py

Created by Steve McMahon on 2009-08-12.
Copyright (c) 2009 Plone Foundation.
"""

import re

from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import \
    IContentish, IMinimalDublinCore, IWorkflowAware, IDublinCore, \
    ICatalogableDublinCore

from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.i18nl10n import ulocalized_time

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
        return safe_unicode(self.context.Title())


class DescriptionSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return safe_unicode(self.context.Description())


class TypeSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return self.context.Type()

class CreatorsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( ', '.join(self.context.listCreators()) )


class ContributorsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( ', '.join(self.context.listContributors()) )


class SubjectSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( ', '.join(self.context.Subject()) )
#


class FormatSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Format() )
#


class LanguageSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Language() )
#


class IdentifierSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Identifier() )
#


class RightsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Rights() )
#


class ReviewStateSubstitution(BaseSubstitution):
    adapts(IWorkflowAware)
    
    def __call__(self):
        wft = getToolByName(self.context, 'portal_workflow')
        return safe_unicode(wft.getInfoFor(self.context, 'review_state'))


class CreatedSubstitution(BaseSubstitution):
    adapts(ICatalogableDublinCore)
    
    def __call__(self):
        return safe_unicode( ulocalized_time(self.context.created()) )


class EffectiveSubstitution(BaseSubstitution):
    adapts(ICatalogableDublinCore)

    def __call__(self):
        return safe_unicode( ulocalized_time(self.context.effective()) )


class ExpiresSubstitution(BaseSubstitution):
    adapts(ICatalogableDublinCore)

    def __call__(self):
        return safe_unicode( ulocalized_time(self.context.expires()) )


class ModifiedSubstitution(BaseSubstitution):
    adapts(ICatalogableDublinCore)

    def __call__(self):
        return safe_unicode( ulocalized_time(self.context.modified()) )
